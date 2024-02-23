import unittest
from Simulator import Simulator, Event, Scheduler, Network

class TestSimulator(unittest.TestCase):

    def test_initialize_events(self):
        """
        Test the initialization of events to ensure the correct number of events is initialized.
        """
        # Initialize the Simulator
        simulator = Simulator()
        # Define the expected number of events
        num_events = 100
        # Initialize events
        simulator.initialize_events(num_events)
        # Check if the number of initialized events matches the expected count
        self.assertEqual(len(simulator.scheduler.events), num_events)

    def test_run_simulation(self):
        """
        Test the simulation process to ensure that it runs correctly.
        """
        # Initialize the Simulator
        simulator = Simulator()
        # Add mock events to the scheduler
        simulator.scheduler.schedule_event(Event("arrival", 10))
        simulator.scheduler.schedule_event(Event("departure", 20))
        # Run the simulation
        simulator.run_simulation()
        # Check if the counts of arrival and departure events are correct
        self.assertEqual(simulator.arrival_count, 1)
        self.assertEqual(simulator.departure_count, 1)

    def test_calculate_average_latency(self):
        """
        Test the calculation of the average latency of packet transmissions.
        """
        # Initialize the Simulator
        simulator = Simulator()
        # Add mock departure events
        simulator.departure_count = 10
        simulator.total_latency = 100
        # Calculate the average latency
        average_latency = simulator.calculate_average_latency()
        # Check if the calculated average latency is correct
        self.assertEqual(average_latency, 10)

    def test_get_nodes_count(self):
        """
        Test the retrieval of the number of nodes in the network to ensure it matches the expected count.
        """
        # Initialize the Network
        network = Network()
        # Generate a Barabasi-Albert topology with 100 nodes
        network.generate_barabasi_albert_topology(n=100, m=2)
        # Check if the number of nodes matches the expected count
        self.assertEqual(network.graph.number_of_nodes(), 100)

    def test_get_events_count(self):
        """
        Test the retrieval of the number of events in the scheduler to ensure it matches the expected count.
        """
        # Initialize the Scheduler
        scheduler = Scheduler()
        # Add 100 events to the scheduler
        for i in range(100):
            scheduler.schedule_event(Event("arrival", i))
        # Check if the number of events matches the expected count
        self.assertEqual(len(scheduler.events), 100)

    def test_arrival_count(self):
        """
        Test the calculation of the arrival count during the simulation.
        """
        # Initialize the Simulator
        simulator = Simulator()
        # Add mock events to the scheduler
        simulator.scheduler.schedule_event(Event("arrival", 10))
        simulator.scheduler.schedule_event(Event("arrival", 20))
        # Run the simulation
        simulator.run_simulation()
        # Check if the calculated arrival count is correct
        self.assertEqual(simulator.arrival_count, 2)

    def test_departure_count(self):
        """
        Test the calculation of the departure count during the simulation.
        """
        # Initialize the Simulator
        simulator = Simulator()
        # Add mock events to the scheduler
        simulator.scheduler.schedule_event(Event("departure", 10))
        simulator.scheduler.schedule_event(Event("departure", 20))
        # Run the simulation
        simulator.run_simulation()
        # Check if the calculated departure count is correct
        self.assertEqual(simulator.departure_count, 2)

if __name__ == '__main__':
    unittest.main()
