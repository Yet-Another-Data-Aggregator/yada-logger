from src.channel import Channel

# A list of all currently loaded channels.
channels = {}


def load_from_config(config):
    """Add all channels listed in config."""
    for key in filter(lambda section: section.startswith("channel/"), config.sections()):
        add_channel(Channel.from_config(config[key]))


def add_channel(channel):
    """Adds the given channel to this manager"""
    channels[channel.name] = channel


def get_channel_cache(channel_name):
    """Returns the logged value cache of the given channel"""
    return channels[channel_name].cache