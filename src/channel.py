from pathlib import Path

import file_utils

class ChannelManager:
    def __init__(self):
        self.channels = {}

    def add_channel(self, channel):
        self.channels[channel.name] = channel

    def get_last_value_for_channel(self, channel_name):
        return self.channels[channel_name].last_value


class Channel:
    """Channel represents the logic that converts sensor data into a logged value."""

    def __init__(self, name, cache_size):
        self.name = name
        self.cache_size = cache_size
        self.cache = []

    @classmethod
    def from_config(cls, config):
        return cls(
            config.name.replace("channel/", ""),
            config.get("cache_size", 0),
        )

    def __repr__(self):
        return f"Channel[name: {self.name}, cache_size: {self.cache_size}, cache: {self.cache}]"

    def write_to_config(self, config):
        config[f"channel/{self.name}"] = {
            "cache_size": self.cache_size
        }

    def next_log_interval(self):
        """Generator that returns the time in milliseconds to wait until the next log. Default is 5 minutes."""
        return 1000 * 60 * 5

    def scan(self):
        """This method generates the actual value to be logged. The return type should be a dict with string keys and
        values that are serializable. Any exceptions that occur while this method is running will be caught and
        logged in place of a data value."""
        pass

    def log(self):
        """Runs scan and adds value to cache"""
        try:
            value = self.scan()

            # Add value to cache and pop if cache has reached max size
            if len(self.cache) >= self.cache_size:
                self.cache.pop()
            self.cache.append(value)

            return value
        except Exception as e:
            raise e
