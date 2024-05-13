import heapq


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