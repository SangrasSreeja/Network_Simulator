import heapq
import random
import networkx as nx
import numpy as np

class Packet:
    def __init__(self, arrival_time, priority=1):
        self.arrival_time = arrival_time
        self.processing_time = random.uniform(1, 10)
        self.priority = priority

class Event:
    def __init__(self, event_type, time, packet=None):
        self.event_type = event_type
        self.time = time
        self.packet = packet

    def __lt__(self, other):
        return self.time < other.time

class Scheduler:
    def __init__(self, scheduler_type='FIFO', quantum=1):
        self.events = []
        self.scheduler_type = scheduler_type
        self.quantum = quantum
        self.current_index = 0

    def schedule_event(self, event):
        if self.scheduler_type == 'PQ':
            heapq.heappush(self.events, (event.time, event.packet.priority, event))
        else:
            heapq.heappush(self.events, (event.time, event))

    def get_next_event(self):
        if self.events:
            if self.scheduler_type == 'PQ':
                return heapq.heappop(self.events)[-1]
            elif self.scheduler_type == 'RR':
                current_event = self.events[self.current_index][-1]
                del self.events[self.current_index]
                if len(self.events) > 0:
                    self.current_index %= len(self.events)
                return current_event
            else:
                return heapq.heappop(self.events)[-1]
        return None

    def has_events(self):
        return len(self.events) > 0

class LLQScheduler(Scheduler):
    def __init__(self):
        super().__init__(scheduler_type='LLQ')
        self.high_priority_queue = []
        self.low_priority_queue = []

    def schedule_event(self, event):
        if event.packet.priority == 1:
            heapq.heappush(self.high_priority_queue, (event.time, event))
        else:
            heapq.heappush(self.low_priority_queue, (event.time, event))

    def get_next_event(self):
        if self.high_priority_queue:
            return heapq.heappop(self.high_priority_queue)[-1]
        elif self.low_priority_queue:
            return heapq.heappop(self.low_priority_queue)[-1]
        else:
            return None

    def has_events(self):
        return len(self.high_priority_queue) > 0 or len(self.low_priority_queue) > 0

class Network:
    def __init__(self):
        self.graph = nx.Graph()
        self.links = {}

    def generate_barabasi_albert_topology(self, n, m):
        self.graph = nx.barabasi_albert_graph(n, m)
        self.initialize_links()

    def initialize_links(self):
        for u, v in self.graph.edges():
            self.links[(u, v)] = {"bandwidth": np.random.uniform(10, 100), "latency": np.random.uniform(1, 10)}
            self.links[(v, u)] = self.links[(u, v)]

class Simulator:
    def __init__(self, max_queue_size=50, scheduler_type='FIFO', quantum=5):
        self.scheduler_type = scheduler_type
        if scheduler_type == 'LLQ':
            self.scheduler = LLQScheduler()
        else:
            self.scheduler = Scheduler(scheduler_type=scheduler_type, quantum=quantum)
        self.packet_queues = [[]]
        self.network = Network()
        self.max_queue_size = max_queue_size
        self.arrival_count = 0
        self.departure_count = 0
        self.dropped_packets = 0
        self.total_latency = 0
        self.latency_list = []
        self.simulation_end_time = 0

    def initialize_events(self, num_events=100):
        for _ in range(num_events):
            time = random.uniform(0, 100)
            priority = random.randint(1, 2)  # Randomly assign priorities (1 or 2)
            packet = Packet(arrival_time=time, priority=priority)
            self.scheduler.schedule_event(Event("arrival", time, packet))

    def run_simulation(self):
        while self.scheduler.has_events():
            event = self.scheduler.get_next_event()
            if isinstance(event, Event) and event.event_type == "arrival":
                self.arrival_count += 1
                if len(self.packet_queues) < self.max_queue_size:
                    self.packet_queues.append(event.packet)
                    departure_time = event.time + event.packet.processing_time
                    self.scheduler.schedule_event(Event("departure", departure_time, event.packet))
                else:
                    self.dropped_packets += 1  # Increment dropped packet count
            elif isinstance(event, Event) and event.event_type == "departure":
                if event.packet in self.packet_queues:
                    self.packet_queues.remove(event.packet)
                    self.departure_count += 1
                    self.total_latency += event.time - event.packet.arrival_time
                    self.latency_list.append(event.time - event.packet.arrival_time)
                    self.simulation_end_time = max(self.simulation_end_time, event.time)

    def calculate_metrics(self):
        simulation_duration = self.simulation_end_time if self.simulation_end_time > 0 else 1
        throughput = self.departure_count / simulation_duration
        average_latency = self.total_latency / self.departure_count if self.departure_count > 0 else 0
        jitter = np.std(self.latency_list) if self.latency_list else 0
        packet_drop_rate = self.dropped_packets / self.arrival_count if self.arrival_count > 0 else 0
        return throughput, average_latency, jitter, packet_drop_rate

# Example usage for FIFO scheduling
fifo_simulator = Simulator(max_queue_size=50, scheduler_type='FIFO')
fifo_simulator.network.generate_barabasi_albert_topology(n=10, m=2)
fifo_simulator.initialize_events(num_events=1000)
fifo_simulator.run_simulation()
fifo_metrics = fifo_simulator.calculate_metrics()
print("FIFO Scheduling Results:")
print(f"Throughput: {fifo_metrics[0]:.2f} packets/unit time")
print(f"Average Latency: {fifo_metrics[1]:.2f} time units")
print(f"Jitter: {fifo_metrics[2]:.2f} time units")
print(f"Packet Drop Rate: {fifo_metrics[3] * 100:.2f}%")

# Example usage for Priority Queue (PQ) scheduling
pq_simulator = Simulator(max_queue_size=50, scheduler_type='PQ')
pq_simulator.network.generate_barabasi_albert_topology(n=10, m=2)
pq_simulator.initialize_events(num_events=1000)
pq_simulator.run_simulation()
pq_metrics = pq_simulator.calculate_metrics()
print("\nPriority Queue (PQ) Scheduling Results:")
print(f"Throughput: {pq_metrics[0]:.2f} packets/unit time")
print(f"Average Latency: {pq_metrics[1]:.2f} time units")
print(f"Jitter: {pq_metrics[2]:.2f} time units")
print(f"Packet Drop Rate: {pq_metrics[3] * 100:.2f}%")

# Example usage for Round Robin scheduling
rr_simulator = Simulator(max_queue_size=50, scheduler_type='RR', quantum=5)
rr_simulator.network.generate_barabasi_albert_topology(n=10, m=2)
rr_simulator.initialize_events(num_events=1000)
rr_simulator.run_simulation()
rr_metrics = rr_simulator.calculate_metrics()
print("\nRound Robin Scheduling Results:")
print(f"Throughput: {rr_metrics[0]:.2f} packets/unit time")
print(f"Average Latency: {rr_metrics[1]:.2f} time units")
print(f"Jitter: {rr_metrics[2]:.2f} time units")
print(f"Packet Drop Rate: {rr_metrics[3] * 100:.2f}%")

# Example usage for Random Early Detection (RED) scheduling
red_simulator = Simulator(max_queue_size=50, scheduler_type='RED')
red_simulator.network.generate_barabasi_albert_topology(n=10, m=2)
red_simulator.initialize_events(num_events=1000)
red_simulator.run_simulation()
red_metrics = red_simulator.calculate_metrics()
print("\nRandom Early Detection (RED) Scheduling Results:")
print(f"Throughput: {red_metrics[0]:.2f} packets/unit time")
print(f"Average Latency: {red_metrics[1]:.2f} time units")
print(f"Jitter: {red_metrics[2]:.2f} time units")
print(f"Packet Drop Rate: {red_metrics[3] * 100:.2f}%")

# Example usage for Low Latency Queuing (LLQ) scheduling
llq_simulator = Simulator(max_queue_size=50, scheduler_type='LLQ')
llq_simulator.network.generate_barabasi_albert_topology(n=10, m=2)
llq_simulator.initialize_events(num_events=1000)
llq_simulator.run_simulation()
llq_metrics = llq_simulator.calculate_metrics()
print("\nLow Latency Queuing (LLQ) Scheduling Results:")
print(f"Throughput: {llq_metrics[0]:.2f} packets/unit time")
print(f"Average Latency: {llq_metrics[1]:.2f} time units")
print(f"Jitter: {llq_metrics[2]:.2f} time units")
print(f"Packet Drop Rate: {llq_metrics[3] * 100:.2f}%")
