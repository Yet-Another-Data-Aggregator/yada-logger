from src.channel import Channel

# A dict of all currently loaded channels keyed by name.
channels = {}

# A dict containing lists of channels keyed by the amount of time before their next run.
next_run_times = {}


def load_from_config(config):
    """Add all channels listed in config."""
    for key in filter(lambda section: section.startswith("channel/"), config.sections()):
        add_channel(Channel.from_config(config[key]))


def add_channel(channel):
    """Adds the given channel to this manager"""
    channels[channel.name] = channel
    add_to_next_run(channel.name, 0)


def get_channel_cache(channel_name):
    """Returns the logged value cache of the given channel"""
    return channels[channel_name].cache


def run_channels():
    """Runs the channels that need run and returns the amount of time to sleep until next log."""

    # Get key of channel first to run
    next_key = sorted(next_run_times)[0]

    for channel_name in next_run_times.pop(next_key, None):
        channel = channels[channel_name]

        # Run channels and log values
        try:
            channel_value = channel.log()
            # TODO log channel value and handle error
            print(channel_value)
        except Exception as e:
            print(e)

        # Get next time to run channel and add back into next_run_times
        try:
            channel_next_run_time = channel.next_log_interval()
        except Exception:
            channel_next_run_time = 1000 * 60 * 5

        add_to_next_run(channel_name, channel_next_run_time)

    # Return time to wait until next run
    return sorted(next_run_times)[0]


def add_to_next_run(channel_name, wait_time):
    """Adds the given channel name to next_run_times with the given time."""
    if wait_time not in next_run_times:
        next_run_times[wait_time] = []
    next_run_times[wait_time].append(channel_name)
