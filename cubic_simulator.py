import random
import numpy as np
from leackyBucket import LeakyBucket
from cubic import Cubic
from cubic import Vegas

from scheduler import Scheduler
from leackyBucket import LeakyBucket
from event import Event
from scheduler import Scheduler
from packet import Packet
from network import Network


import csv

class Simulator:
    def __init__(self, max_queue_size=50, scheduler_type='FIFO', quantum=5, rate=10, capacity=100,algo = 'cubic'):
        self.scheduler_type = scheduler_type
        self.cwnd = None
        self.scheduler = Scheduler(scheduler_type=scheduler_type, quantum=quantum)
        self.leaky_bucket = LeakyBucket(rate, capacity)
        if algo == 'cubic':
            self.cubic = Cubic()
        else:
            self.cubic = Vegas()
            # new_cwnd = self.cubic.update_cwnd()

            # # Print the updated congestion window size
            # print("Updated congestion window size:", new_cwnd)

 
        self.flows = {'flow1': [], 'flow2': []}
        self.network = Network()
        self.max_queue_size = max_queue_size
        self.arrival_counts = {'flow1': 0, 'flow2': 0}
        self.departure_counts = {'flow1': 0, 'flow2': 0}
        self.dropped_packets = {'flow1': 0, 'flow2': 0}
        self.total_latencies = {'flow1': 0, 'flow2': 0}
        self.latency_lists = {'flow1': [], 'flow2': []}
        self.simulation_end_times = {'flow1': 0, 'flow2': 0}
        self.metrics_per_second = {flow_id: {} for flow_id in self.flows}

    def initialize_events(self, num_events=100, flow_id='flow1'):
        for _ in range(num_events):
            event_time = random.uniform(0, 100)
            priority = random.randint(1, 2)
            packet = Packet(arrival_time=event_time, priority=priority)
            self.scheduler.schedule_event(Event("arrival", event_time, packet, flow_id=flow_id))

    def run_simulation(self):
        current_second = 0
        while self.scheduler.has_events():
            
            self.cwnd = self.cubic.update_cwnd()
            event = self.scheduler.get_next_event()
            current_second = int(event.time)  # Convert event time to an integer second

            if isinstance(event, Event) and event.event_type == "arrival":
                flow_id = event.flow_id
                self.arrival_counts[flow_id] += 1
                if self.leaky_bucket.remove_tokens(1) and len(self.flows[flow_id]) < self.cubic.cwnd:
                    self.flows[flow_id].append(event.packet)
                    departure_time = event.time + event.packet.processing_time
                    self.scheduler.schedule_event(Event("departure", departure_time, event.packet, flow_id=flow_id))
                else:
                    self.dropped_packets[flow_id] += 1
                    self.cubic.congestion_event()
            elif isinstance(event, Event) and event.event_type == "departure":
                flow_id = event.flow_id
                if event.packet in self.flows[flow_id]:
                    # print(",,,,,,,,,,,,,,",event.packet)
                    self.flows[flow_id].remove(event.packet)
                    self.departure_counts[flow_id] += 1
                    latency = event.time - event.packet.arrival_time
                    self.total_latencies[flow_id] += latency
                    self.latency_lists[flow_id].append(latency)
                    self.simulation_end_times[flow_id] = max(self.simulation_end_times[flow_id], event.time)


                    # Calculate jitter
                    if len(self.latency_lists[flow_id]) >= 2:
                        jitter = self.latency_lists[flow_id][-1] - self.latency_lists[flow_id][-2]
                    else:
                        jitter = 0

                    # Calculate packet drop rate
                    total_packets_sent = self.arrival_counts[flow_id]
                    total_packets_dropped = self.dropped_packets[flow_id]
                    packet_drop_rate = total_packets_dropped / total_packets_sent if total_packets_sent > 0 else 0

                    # Track per-second metrics

                    if current_second not in self.metrics_per_second[flow_id]:
                        self.metrics_per_second[flow_id][current_second] = {'throughput': 0, 'total_latency': 0, 'jitter': 0, 'packet_drop_rate': 0}
                    self.metrics_per_second[flow_id][current_second]['throughput'] += 1
                    self.metrics_per_second[flow_id][current_second]['total_latency'] += latency
                    self.metrics_per_second[flow_id][current_second]['jitter'] = jitter
                    self.metrics_per_second[flow_id][current_second]['packet_drop_rate'] = packet_drop_rate
                    # if current_second not in self.metrics_per_second[flow_id]:
                    #     self.metrics_per_second[flow_id][current_second] = {'throughput': 0, 'total_latency': 0}
                    # self.metrics_per_second[flow_id][current_second]['throughput'] += 1
                    # self.metrics_per_second[flow_id][current_second]['total_latency'] += latency

    def write_metrics_to_csv(self):
        for flow_id, metrics in self.metrics_per_second.items():
            with open(f'{flow_id}_metrics.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                # writer.writerow(['Second', 'Throughput', 'Average Latency'])
                writer.writerow(['Second', 'Throughput', 'Average Latency', 'Jitter', 'Packet Drop Rate'])

                for second in sorted(metrics):
                    throughput = metrics[second]['throughput']
                    total_latency = metrics[second]['total_latency']
                    average_latency = total_latency / throughput if throughput > 0 else 0
                    
                    jitter = metrics[second].get('jitter', 0)
                    packet_drop_rate = metrics[second].get('packet_drop_rate', 0)
                    writer.writerow([second, throughput, average_latency, jitter, packet_drop_rate])

                    # writer.writerow([second, throughput, average_latency])

# Example usage
sim = Simulator(max_queue_size=100, scheduler_type='RR', rate=5, capacity=50,algo='vegas')
sim.initialize_events(num_events=1000000, flow_id='flow1')
sim.initialize_events(num_events=10000, flow_id='flow2')
sim.run_simulation()
sim.write_metrics_to_csv()
import matplotlib.pyplot as plt

time_data = []
latency_data = []
throughput_data = []
jitter_data = []
packet_drop_data = []

# Extract data for plotting
for flow_id, metrics in sim.metrics_per_second.items():
    for second, metric_data in metrics.items():
        # Append time data
        time_data.append(second)
        # Append latency data
        latency_data.append(metric_data.get('total_latency', 0))
        # Append throughput data
        throughput_data.append(metric_data.get('throughput', 0))
        # Append jitter data
        jitter_data.append(metric_data.get('jitter', 0))
        # Append packet drop data
        packet_drop_data.append(metric_data.get('packet_drop_rate', 0))

# Plot total latency
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
plt.plot(time_data, latency_data, label='Total Latency')
plt.xlabel('Time (seconds)')
plt.ylabel('Total Latency')
plt.title('Total Latency over Time')
plt.legend()
plt.grid(True)

# Plot throughput
plt.subplot(2, 2, 2)
plt.plot(time_data, throughput_data, label='Throughput')
plt.xlabel('Time (seconds)')
plt.ylabel('Throughput')
plt.title('Throughput over Time')
plt.legend()
plt.grid(True)

# Plot jitter
plt.subplot(2, 2, 3)
plt.plot(time_data, jitter_data, label='Jitter')
plt.xlabel('Time (seconds)')
plt.ylabel('Jitter')
plt.title('Jitter over Time')
plt.legend()
plt.grid(True)

# Plot packet drop rate
plt.subplot(2, 2, 4)
plt.plot(time_data, packet_drop_data, label='Packet Drop Rate')
plt.xlabel('Time (seconds)')
plt.ylabel('Packet Drop Rate')
plt.title('Packet Drop Rate over Time')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()




#num_events=100000000
#(num_events=100000
#max_queue_size=1000