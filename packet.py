import random

class Packet:
    def __init__(self, arrival_time, priority=1):
        self.arrival_time = arrival_time
        self.processing_time = random.uniform(1, 10)
        self.priority = priority