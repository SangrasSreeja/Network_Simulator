from Simulator import Simulator  # Import the Simulator class from Simulator module

simulator = Simulator()  # Instantiate the Simulator object

# Generate network topology using Waxman model with Experiment 2 parameters
simulator.network.generate_waxman_topology(n=200, alpha=0.57, beta=0.1)  # Adjusted to generate 1000 links (n=200)

# Initialize events for Experiment 2 (1000 events)
simulator.initialize_events(num_events=1000)  # Initialize 1000 simulation events

# Print the counts of nodes, links, and events
print(f"Number of nodes: {simulator.get_nodes_count()}")  # Print the count of nodes in the network
print(f"Number of links: {simulator.get_links_count()}")  # Print the count of links in the network
print(f"Number of events: {simulator.get_events_count()}")  # Print the count of events in the simulation

# Run simulation
simulator.run_simulation()  # Run the simulation

# Calculate and report statistics
average_latency = simulator.calculate_average_latency()  # Calculate the average latency of packet transmissions
print(f"Total packets arrived: {simulator.arrival_count}")  # Print the total count of packet arrivals
print(f"Total packets departed: {simulator.departure_count}")  # Print the total count of packet departures
print(f"Average latency: {average_latency}")  # Print the average latency of packet transmissions
