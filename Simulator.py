import heapq
import random
import networkx as nx
import numpy as np

class Packet:
    """Represents a network packet with an arrival time and processing time."""
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.processing_time = random.uniform(1, 10)  # Simulate processing time

class Event:
    """Represents an event in the simulation, such as a packet's arrival or departure."""
    def __init__(self, event_type, time, packet=None):
        self.event_type = event_type  # "arrival" or "departure"
        self.time = time  # When the event occurs
        self.packet = packet  # The packet associated with the event, if any

    def __lt__(self, other):
        # This ensures that the priority queue can order events based on their time
        return self.time < other.time

class Scheduler:
    """Manages the scheduling and processing of events in the simulation."""
    def __init__(self):
        self.events = []  # A priority queue (heap) of events

    def schedule_event(self, event):
        # Adds an event to the queue
        heapq.heappush(self.events, event)

    def get_next_event(self):
        # Retrieves and removes the next event from the queue, if available
        if self.events:
            return heapq.heappop(self.events)
        return None

    def has_events(self):
        # Checks if there are any events left to process
        return len(self.events) > 0

class Network:
    """Represents the network topology."""
    def __init__(self):
        self.graph = nx.Graph()  # Use NetworkX to manage the graph
        self.links = {}  # Stores properties of links between nodes

    def generate_barabasi_albert_topology(self, n, m):
        # Generates a scale-free network using the Barabási-Albert model
        self.graph = nx.barabasi_albert_graph(n, m)
        self.initialize_links()

    def initialize_links(self):
        # Initializes the links between nodes with random bandwidth and latency
        for u, v in self.graph.edges():
            self.links[(u, v)] = {"bandwidth": np.random.uniform(10, 100), "latency": np.random.uniform(1, 10)}
            self.links[(v, u)] = self.links[(u, v)]  # Assume symmetric links

class Simulator:
    """Main class for running the network simulation."""
    def __init__(self, max_queue_size=50):
        self.scheduler = Scheduler()
        self.network = Network()
        self.packet_queue = []  # Queue to hold packets waiting for processing
        self.max_queue_size = max_queue_size  # Maximum packets the queue can hold
        self.arrival_count = 0  # Total number of packet arrivals
        self.departure_count = 0  # Total number of packet departures
        self.dropped_packets = 0  # Total number of dropped packets
        self.total_latency = 0  # Sum of all packet latencies for average calculation
        self.latency_list = []  # List of individual packet latencies for jitter calculation
        self.simulation_end_time = 0  # End time of the last event processed

    def initialize_events(self, num_events=100):
        # Initializes a set number of packet arrival events at random times
        for _ in range(num_events):
            time = random.uniform(0, 100)
            packet = Packet(arrival_time=time)
            self.scheduler.schedule_event(Event("arrival", time, packet))

    def run_simulation(self):
        # Processes events in the queue until all are handled
        while self.scheduler.has_events():
            event = self.scheduler.get_next_event()
            if event.event_type == "arrival":
                self.arrival_count += 1
                # Check if queue is below capacity before adding packet
                if len(self.packet_queue) < self.max_queue_size:
                    self.packet_queue.append(event.packet)
                    departure_time = event.time + event.packet.processing_time
                    self.scheduler.schedule_event(Event("departure", departure_time, event.packet))
                else:
                    # Packet is dropped if queue is at capacity
                    self.dropped_packets += 1
            elif event.event_type == "departure" and self.packet_queue:
                # Process packet departure
                self.departure_count += 1
                packet = self.packet_queue.pop(0)  # Remove packet from queue
                self.total_latency += event.time - packet.arrival_time  # Calculate latency
                self.latency_list.append(event.time - packet.arrival_time)  # Store latency for jitter calculation
                self.simulation_end_time = max(self.simulation_end_time, event.time)  # Update simulation end time

   
    def calculate_metrics(self):
        """Calculates performance metrics based on simulation results."""
        simulation_duration = self.simulation_end_time if self.simulation_end_time > 0 else 1
        throughput = self.departure_count / simulation_duration  # packets per time unit
        average_latency = self.total_latency / self.departure_count if self.departure_count > 0 else 0
        jitter = np.std(self.latency_list) if self.latency_list else 0  # Variation in latency
        packet_drop_rate = self.dropped_packets / self.arrival_count if self.arrival_count > 0 else 0  # Fraction of packets dropped
        
        return throughput, average_latency, jitter, packet_drop_rate

# Example usage
simulator = Simulator(max_queue_size=50)  # Set maximum queue size
simulator.network.generate_barabasi_albert_topology(n=10, m=2)  # Generate network topology
simulator.initialize_events(num_events=1000)  # Initialize a set of packet arrival events
simulator.run_simulation()  # Run the simulation

# Calculate and print performance metrics
throughput, average_latency, jitter, packet_drop_rate = simulator.calculate_metrics()
print(f"Throughput: {throughput:.2f} packets/unit time, Average Latency: {average_latency:.2f} time units, "
      f"Jitter: {jitter:.2f} time units, Packet Drop Rate: {packet_drop_rate * 100:.2f}%")
