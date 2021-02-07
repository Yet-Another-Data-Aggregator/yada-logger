class ChannelManager:
    def __init__(self):
        self.channels = {}

    def add_channel(self, channel):
        self.channels[channel.name] = channel

    def get_last_value_for_channel(self, channel_name):
        return self.channels[channel_name].last_value


class Channel:
    """Channel represents the logic that converts sensor data into a logged value."""

    def __init__(self, name, channel_type, read_rate):
        self.name = name
        self.channel_type = channel_type
        self.read_rate = read_rate
        self.last_value = {}

    def __repr__(self):
        return f"Device[name: {self.name}, channel_type: {self.channel_type}, read_rate: {self.read_rate}]"

    def write_to_config(self, config):
        config[f"channel/{self.name}"] = {
            "channel_type": self.channel_type,
            "read_rate": self.read_rate
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
        """This method runs scan and handles the logging of the values."""
        try:
            value = self.scan()

            self.last_value = value

            # TODO log value
        except Exception as e:
            print(e)


def from_config(config):
    return Channel(
        config.name.replace("channel/", ""),
        config.get("channel_type", ""),
        config.get("read_rate", 60000),
    )
