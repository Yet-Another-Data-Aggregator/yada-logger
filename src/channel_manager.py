import importlib

from config import Config

CHANNEL_MODULE_PATH = "channels."


class ChannelManager:
    # A dict of all currently loaded channels keyed by name and their modules
    channels = {}

    # A dict containing lists of channels keyed by the amount of time before their next run.
    run_times = {}

    @staticmethod
    def initialize():
        config = Config.get()

        if "config" not in config:
            return

        config = config["config"]

        global CHANNEL_MODULE_PATH

        CHANNEL_MODULE_PATH = config.get("channel_module_path", "channels").replace("/", ".")

    @staticmethod
    def load_from_config(config):
        """Add all channels listed in config."""
        for key in filter(lambda section: section.startswith("channel/"), config.sections()):
            channel_module = importlib.import_module(f"{CHANNEL_MODULE_PATH}{config[key]['module']}")
            ChannelManager.add_channel(ChannelManager.load_channel(key.replace("channel/", ""), channel_module))

    @staticmethod
    def load_channel(channel_name, channel_module):
        channel_class = getattr(channel_module, channel_name)
        setattr(channel_module, "ChannelManager", ChannelManager)

        return channel_class.initialize()

    @staticmethod
    def add_channel(channel):
        """Adds the given channel to this manager"""
        ChannelManager.channels[channel.__class__.__name__] = channel

        add_to_multi_dict(0, channel, ChannelManager.run_times)

    @staticmethod
    def get_channel_cache(channel_name):
        """Returns the logged value cache of the given channel"""
        return ChannelManager.channels[channel_name].cache

    @staticmethod
    def run_channels():
        """Runs the channels that need run and returns the amount of time to sleep until next log."""

        # If no channels to run, return and wait five seconds
        if len(ChannelManager.run_times) == 0:
            return 5

        # Get key of channel first to run
        key = sorted(ChannelManager.run_times)[0]
        channels_to_run = ChannelManager.run_times.pop(key, [])

        next_run_times = {}

        for time, channel_list in ChannelManager.run_times.items():
            add_to_multi_dict(time - key, channel_list, next_run_times)

        for channel in channels_to_run:
            # Run channels and log values
            try:
                value = channel.log()
                # TODO log channel value and handle error
            except Exception as e:
                print(e)

            # Get next time to run channel and add back into next_run_times
            try:
                channel_next_run_time = channel.next_log_interval()
            except Exception:
                channel_next_run_time = 1000 * 60 * 5

            add_to_multi_dict(channel_next_run_time, channel, next_run_times)

        ChannelManager.run_times = next_run_times

        # Return time to wait until next run
        return sorted(ChannelManager.run_times)[0]


def add_to_multi_dict(key, value, dictionary):
    """Adds the given channel name to next_run_times with the given time."""
    if key not in dictionary:
        dictionary[key] = []

    if isinstance(value, list):
        dictionary[key].extend(value)
    else:
        dictionary[key].append(value)
