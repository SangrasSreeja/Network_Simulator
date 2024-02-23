from Simulator import Simulator  # Import the Simulator class from Simulator module

simulator = Simulator()  # Instantiate the Simulator object

simulator.network.generate_barabasi_albert_topology(n=100, m=6)  # Generate Barabasi-Albert network topology with 100 nodes and average degree 6

simulator.initialize_events(num_events=100)  # Initialize 100 simulation events

print(f"Number of nodes: {simulator.get_nodes_count()}")  # Print the count of nodes in the network
print(f"Number of links: {simulator.get_links_count()}")  # Print the count of links in the network
print(f"Number of events: {simulator.get_events_count()}")  # Print the count of events in the simulation

simulator.run_simulation()  # Run the simulation

average_latency = simulator.calculate_average_latency()  # Calculate the average latency of packet transmissions
print(f"Total packets arrived: {simulator.arrival_count}")  # Print the total count of packet arrivals
print(f"Total packets departed: {simulator.departure_count}")  # Print the total count of packet departures
print(f"Average latency: {average_latency}")  # Print the average latency of packet transmissions
