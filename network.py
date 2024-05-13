import networkx as nx
import numpy as np

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
