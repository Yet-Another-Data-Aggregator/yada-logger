class ScanException(Exception):
    pass


class ChannelManager:
    def __init__(self):
        self.channels = {}

    def add_channel(self, channel):
        self.channels[channel.name] = channel

    def get_last_value_for_channel(self, channel_name):
        return self.channels[channel_name].last_value


class Channel:
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

    def scan(self):
        """Should return a map with the name of the value and the actual value"""
        pass

    def log(self):
        try:
            value = self.scan()

            self.last_value = value

            # TODO log value
        except ScanException as e:
            print(e)


def from_config(config):
    return Channel(
        config.name.replace("channel/", ""),
        config.get("channel_type", ""),
        config.get("read_rate", 60000),
    )
