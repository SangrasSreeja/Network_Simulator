import heapq
import random
import networkx as nx
import numpy as np

# Event Class
class Event:
    def __init__(self, event_type, time):
        self.event_type = event_type  # Type of event: "arrival" or "departure"
        self.time = time  # Time at which the event occurs

    def __lt__(self, other):
        return self.time < other.time

# Scheduler Class
class Scheduler:
    def __init__(self):
        self.events = []  # Priority queue to store events

    def schedule_event(self, event):
        heapq.heappush(self.events, event)  # Add event to the priority queue

    def get_next_event(self):
        if self.events:
            return heapq.heappop(self.events)  # Get the next event from the priority queue
        else:
            return None

    def has_events(self):
        return len(self.events) > 0  # Check if there are any events in the queue

# Network Class
class Network:
    def __init__(self):
        self.graph = nx.Graph()  # Initialize empty graph
        self.links = {}  # Dictionary to store link properties

    # Generate network topology using the Barabasi-Albert model
    def generate_barabasi_albert_topology(self, n, m):
        self.graph = nx.barabasi_albert_graph(n, m)  # Generate Barabasi-Albert graph
        self.initialize_links()  # Initialize links with default properties

    # Generate network topology using the Waxman model
    def generate_waxman_topology(self, n, alpha=0.4, beta=0.1):
        self.graph = nx.waxman_graph(n, alpha=alpha, beta=beta)  # Generate Waxman graph
        self.initialize_links()  # Initialize links with default properties

    # Initialize links with default properties
    def initialize_links(self):
        for u, v in self.graph.edges():
            self.links[(u, v)] = {"bandwidth": np.random.uniform(10, 100), "latency": np.random.uniform(1, 10)}
            self.links[(v, u)] = self.links[(u, v)]  # Assuming symmetrical links

    # Add a new link with specified properties
    def add_link(self, source, destination, bandwidth, latency):
        self.links[(source, destination)] = {"bandwidth": bandwidth, "latency": latency}
        self.links[(destination, source)] = {"bandwidth": bandwidth, "latency": latency}  # Symmetrical link

    # Get properties of a specific link
    def get_link_properties(self, source, destination):
        return self.links.get((source, destination), None)

# Simulator Class
class Simulator:
    def __init__(self):
        self.scheduler = Scheduler()  # Initialize scheduler
        self.network = Network()  # Initialize network
        self.arrival_count = 0  # Count of packet arrivals
        self.departure_count = 0  # Count of packet departures
        self.total_latency = 0  # Total latency for all packets

    # Initialize simulation events
    def initialize_events(self, num_events=100):
        for _ in range(num_events):
            event_type = random.choice(["arrival", "departure"])  # Randomly select event type
            time = random.uniform(0, 100)  # Random time
            self.scheduler.schedule_event(Event(event_type, time))  # Schedule the event
    def get_nodes_count(self):
       return len(self.network.graph.nodes)
    
    def get_links_count(self):
        return len(self.network.graph.edges)
    
    def get_events_count(self):
        return sum(1 for _ in self.scheduler.events)
    
    # Run the simulation
    def run_simulation(self):
        global_simulator_time = 0  # Global simulation time
        while self.scheduler.has_events():
            event = self.scheduler.get_next_event()  # Get next event from scheduler
            global_simulator_time = event.time  # Update global simulation time
            if event.event_type == "arrival":
                self.arrival_count += 1  # Increment arrival count
                print(f"Packet arrived at time {event.time}")  # Print arrival event
            elif event.event_type == "departure":
                self.departure_count += 1  # Increment departure count
                print(f"Packet departed at time {event.time}")  # Print departure event

    # Calculate the average latency of packet transmissions
    def calculate_average_latency(self):
        return self.total_latency / self.departure_count if self.departure_count > 0 else 0