from channel import Channel
import random


class RandomChannel(Channel):
    def __init__(self):
        super().__init__()

        self.cache_size = 1

    def next_log_interval(self):
        return 2

    def scan(self):
        return {"random_value": random.randrange(100)}
