import importlib
from datetime import datetime

import json
import config
import file_utils
from file_utils import Files


# The module path to import from
channel_module_path = "channels."


@config.section("storage")
def load_variables(section):
    """
    Loads configuration variables from the "storage" section

    :param section: The configuration section
    """
    global channel_module_path
    channel_module_path = section.get("channel_module_directory", "channels/").replace("/", ".")


class ChannelManager:
    """
    Static utility class to manage loading and running of channels.
    """

    # A dict of all currently loaded channels keyed by name
    channels = {}

    # A dict containing lists of channels keyed by the amount of time before their next run.
    run_times = {}

    @staticmethod
    def initialize():
        """
        Loads configuration variables
        """
        load_variables()

    @staticmethod
    def load_from_config(config_object):
        """
        Add all channels listed in config.

        :param config_object: The configuration object to load channels from.
        """
        for key in filter(lambda section: section.startswith("channel/"), config_object.sections()):
            channel_module = importlib.import_module(f"{channel_module_path}{config_object[key]['module']}")
            ChannelManager.add_channel(ChannelManager.load_channel(key.replace("channel/", ""), channel_module))

    @staticmethod
    def load_channel(channel_name, channel_module):
        """
        Loads the channel with the given name from the given module and ensures that the ChannelManager is set in the
        loaded class' globals.

        :param channel_name: The name of the class of the channel to load.
        :param channel_module: The module to load the channel class from.
        :return: A new instance of the channel object.
        """
        channel_class = getattr(channel_module, channel_name)
        setattr(channel_module, "ChannelManager", ChannelManager)

        return channel_class.initialize()

    @staticmethod
    def add_channel(channel):
        """
        Adds the given channel to this manager.

        :param channel: The channel object to add.
        """
        ChannelManager.channels[channel.__class__.__name__] = channel
        add_to_multi_dict(0, channel, ChannelManager.run_times)

    @staticmethod
    def get_channel_cache(channel_name):
        """
        Returns the logged value cache of the given channel.

        :param channel_name: The name of the channel to get the cache from.
        """
        return ChannelManager.channels[channel_name].cache

    @staticmethod
    def run_channels():
        """
        Runs the channels that need run and returns the amount of time to sleep until next log.
        """
        result_values = {}
        result_faults = []
        next_run_times = {}

        # If no channels to run, return and wait five seconds
        if len(ChannelManager.run_times) == 0:
            return 5

        # Get key of channel first to run
        key = sorted(ChannelManager.run_times)[0]
        channels_to_run = ChannelManager.run_times.pop(key, [])

        # Updates times of channels that haven't been run
        for time, channel_list in ChannelManager.run_times.items():
            add_to_multi_dict(time - key, channel_list, next_run_times)

        for channel in channels_to_run:
            # Run channels and log values
            try:
                value = channel.log()

                if isinstance(value, dict):
                    result_values.update(value)
                elif isinstance(value, tuple):
                    result_values.update(value[0])
                    result_faults.append(value[1])
                elif isinstance(value, list):
                    result_faults.append(value)
            except Exception as e:
                result_faults.append(repr(e))

            # Get next time to run channel and add back into next_run_times
            try:
                channel_next_run_time = channel.next_log_interval()
            except Exception:
                channel_next_run_time = 1000 * 60 * 5

            add_to_multi_dict(channel_next_run_time, channel, next_run_times)

        # Set timestamps
        now = datetime.now().strftime(file_utils.date_format)
        result_values["timestamp"] = now

        if result_faults:
            result_faults = {
                "timestamp": now,
                "messages": result_faults
            }

            with Files.get_append_log_file(file_utils.logging_directory, "faults") as file:
                file.write(json.dumps(result_faults))
                file.write("\n")
                Files.close(file)

            with Files.get_append_log_file(file_utils.fault_upload_directory, "fault_upload") as file:
                file.write(json.dumps(result_faults))
                file.write("\n")
                Files.close(file)

        with Files.get_append_log_file(file_utils.logging_directory, "values") as file:
            file.write(json.dumps(result_values))
            file.write("\n")
            Files.close(file)

        with Files.get_append_upload_file(file_utils.value_upload_directory, "upload") as file:
            file.write(json.dumps(result_values))
            file.write("\n")
            Files.close(file)

        ChannelManager.run_times = next_run_times

        # Return time to wait until next run
        return sorted(ChannelManager.run_times)[0]


def add_to_multi_dict(key, value, dictionary):
    """
    Adds the given value to the given multi-dictionary associated with the given key.
    """
    if key not in dictionary:
        dictionary[key] = []

    if isinstance(value, list):
        dictionary[key].extend(value)
    else:
        dictionary[key].append(value)
