from channel import Channel
from datetime import datetime


class TimeChannel(Channel):
    def next_log_interval(self):
        return 30

    def scan(self):
        result = datetime.now()

        print(result)

        return {"time", result}
