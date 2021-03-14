import os
import sys
import time
import importlib

import config
import network
from channel_manager import ChannelManager
from config import Config
from file_utils import Files


# Name of datastore to load
datastore = None

# If false nothing will be uploaded
should_upload = False

# Interval in seconds between checks to update channels
template_update_interval = 60 * 5

# Controls if the application should restart or quit
restart = False

# Indicates whether the application is running
running = True


@config.section("config")
def load_variables(section):
    """
    Loads variables from the "config" section of the configuration file

    :param section: The config section
    """
    global template_update_interval, datastore, should_upload
    template_update_interval = float(section.get("template_refresh_interval", 60 * 5))

    should_upload = section.get("should_upload", False)

    datastore_module = importlib.import_module(f"{section['datastore_module']}")
    datastore_class = getattr(datastore_module, section['datastore_class'])
    datastore = datastore_class()


def initialize():
    """
    Initializes the application and checks if the channels need updated.
    """
    load_variables()

    Files.initialize()
    ChannelManager.initialize()

    if datastore.should_update_template():
        datastore.fetch()

    ChannelManager.load_from_config(Config.get())


def check_update():
    """
    Checks whether the channels need updating. If not, this function returns without doing anything, if so, the new
    channels are fetched and the running and restart variables are set to reload the application.
    """
    if not datastore.should_update_template():
        return

    datastore.fetch()

    global running, restart
    running = False
    restart = True


def run():
    """
    Main loop of the application. Runs all channels, sleeps until next channel run time, and checks for channel
    updates if the interval is up.
    """
    now = time.time()

    # Run all channels and then sleep until the next channel should run
    while running:
        wait_time, results = ChannelManager.run_channels()

        if should_upload and results:
            datastore.upload_data(results)

        time.sleep(wait_time)

        if time.time() - now > template_update_interval:
            now = time.time()
            check_update()


if __name__ == '__main__':
    initialize()

    run()

    # Restart the process if True
    if restart:
        os.execv(sys.executable, ['python'] + sys.argv)
