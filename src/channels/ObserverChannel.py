from channel import Channel
from channel_manager import ChannelManager


class ObserverChannel(Channel):

    def next_log_interval(self):
        return 2

    def scan(self):
        random_cache = ChannelManager.get_channel_cache("RandomChannel")

        return {"random_greater_than_fifty": True if random_cache[0]["random_value"] > 50 else False}
