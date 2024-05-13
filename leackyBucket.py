import time


class LeakyBucket:
    def __init__(self, rate, capacity):
        self.capacity = capacity
        self.tokens = capacity
        self.rate = rate
        self.last_checked = time.time()

    def add_tokens(self):
        current_time = time.time()
        elapsed = current_time - self.last_checked
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_checked = current_time

    def remove_tokens(self, num_tokens):
        self.add_tokens()
        if num_tokens <= self.tokens:
            self.tokens -= num_tokens
            return True
        return False

