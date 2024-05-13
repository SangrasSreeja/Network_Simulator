class Event:
    def __init__(self, event_type, time, packet=None, flow_id=None):
        self.event_type = event_type
        self.time = time
        self.packet = packet
        self.flow_id = flow_id  # Add flow_id to differentiate events from different flows

    def __lt__(self, other):
        return self.time < other.time
