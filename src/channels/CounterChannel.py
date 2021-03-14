from channel import Channel


class CounterChannel(Channel):
    def __init__(self):
        super().__init__()

        self.value = 0

    def next_log_interval(self):
        return 5

    def scan(self):
        self.value += 1
        return {"counter": self.value}
