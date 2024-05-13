import time
import random

class Cubic:
    def __init__(self, c=0.4, max_cwnd=1000, initial_cwnd=10):
        self.c = c
        self.cwnd = initial_cwnd
        self.max_cwnd = max_cwnd
        self.last_congestion_time = None
        self.origin_point = self.cwnd
        self.time_of_last_update = time.time()
        self.packet_arrival_times = []  # Store packet arrival times
        self.dropped_packets = []  

    def update_cwnd(self):
        if self.last_congestion_time is None:
            return self.cwnd
        t = time.time() - self.last_congestion_time
        w_cubic = self.cubic_function(t)
        self.cwnd = min(w_cubic, self.max_cwnd)
        self.time_of_last_update = time.time()
        return self.cwnd

    def cubic_function(self, t):
        return self.origin_point + self.c * (t ** 3)

    def congestion_event(self):
        self.last_congestion_time = time.time()
        self.origin_point = max(self.cwnd / 2, 1)  # Reduce window by half on congestion
        self.cwnd = self.origin_point
        self.update_cwnd()
        
        
class Vegas(Cubic):
    def __init__(self, c=0.4, max_cwnd=1000, initial_cwnd=10, alpha=0.5, beta=0.3):
        super().__init__(c, max_cwnd, initial_cwnd)
        self.alpha = alpha  # VEGAS alpha value
        self.beta = beta    # VEGAS beta value
        self.base_rtt = 0
        self.smooth_rtt = 0
        self.cwnd = initial_cwnd
        self.max_cwnd = max_cwnd
        self.last_congestion_time = None
        self.packet_arrival_times = []  # Store packet arrival times
        self.dropped_packets = []  

    def update_cwnd(self):
        if self.last_congestion_time is None:
            return self.cwnd
        t = time.time() - self.last_congestion_time
        rtt_sample =random.uniform(10, 100)
        self.update_smooth_rtt(rtt_sample)        
        w_cubic = self.cubic_function(t)
        self.cwnd = min(w_cubic, self.max_cwnd)
        self.time_of_last_update = time.time()
        return self.cwnd


    def update_smooth_rtt(self, rtt_sample):
        if self.base_rtt == 0:
            self.base_rtt = rtt_sample
        else:
            self.smooth_rtt = (1 - self.alpha) * self.smooth_rtt + self.alpha * rtt_sample

    def cubic_function(self, t):
        if self.smooth_rtt < self.base_rtt:
            return self.origin_point + self.c * (t ** 3)
        elif self.smooth_rtt > self.base_rtt:
            return max(self.origin_point - self.beta * (self.base_rtt - self.smooth_rtt), 1)
        else:
            return self.origin_point

    def congestion_event(self):
        super().congestion_event()
        self.base_rtt = self.smooth_rtt = 0  # Reset RTT parameters on congestion event

    def simulate_packet_arrival(self, time):
        # Simulate a packet arrival at time 'time'
        self.packet_arrival_times.append(time)

    def simulate_packet_drop(self, packet_index):
        # Simulate a packet drop
        self.dropped_packets.append(packet_index)
        
    def calculate_jitter(self):
        jitter = [self.packet_arrival_times[i] - self.packet_arrival_times[i-1] 
                  for i in range(1, len(self.packet_arrival_times))]
        avg_jitter = sum(jitter) / len(jitter) if len(jitter) > 0 else 0
        return avg_jitter

    def calculate_packet_drop_rate(self):
        total_packets = len(self.packet_arrival_times) + len(self.dropped_packets)
        packet_drop_rate = len(self.dropped_packets) / total_packets if total_packets > 0 else 0
        return packet_drop_rate

