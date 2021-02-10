import importlib


class ChannelManager:
    # A dict of all currently loaded channels keyed by name.
    channels = {}

    # A dict containing lists of channels keyed by the amount of time before their next run.
    run_times = {}

    @staticmethod
    def load_from_config(config):
        """Add all channels listed in config."""
        for key in filter(lambda section: section.startswith("channel/"), config.sections()):
            channel_module = importlib.import_module("src.channels." + config[key]["module"])
            channel_class = getattr(channel_module, config[key]["class"])

            setattr(channel_module, "ChannelManager", ChannelManager)

            ChannelManager.add_channel(channel_class.from_config(config[key]))

    @staticmethod
    def add_channel(channel):
        """Adds the given channel to this manager"""
        ChannelManager.channels[channel.name] = channel

        add_to_multi_dict(0, channel.name, ChannelManager.run_times)

    @staticmethod
    def get_channel_cache(channel_name):
        """Returns the logged value cache of the given channel"""
        return ChannelManager.channels[channel_name].cache

    @staticmethod
    def run_channels():
        """Runs the channels that need run and returns the amount of time to sleep until next log."""
        # Get key of channel first to run
        next_key = sorted(ChannelManager.run_times)[0]
        next_channels = ChannelManager.run_times.pop(next_key, None)

        next_run_times = {}

        for time, channel_list in ChannelManager.run_times.items():
            add_to_multi_dict(time - next_key, channel_list, next_run_times)

        for channel_name in next_channels:
            channel = ChannelManager.channels[channel_name]

            # Run channels and log values
            try:
                channel_value = channel.log()
                # TODO log channel value and handle error
                print(f"Channel Value: {channel_value}")
            except Exception as e:
                print(e)

            # Get next time to run channel and add back into next_run_times
            try:
                channel_next_run_time = channel.next_log_interval()
                print(f"Channel Next Run Time: {channel_next_run_time}")
            except Exception:
                channel_next_run_time = 1000 * 60 * 5

            add_to_multi_dict(channel_next_run_time, channel_name, next_run_times)

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
