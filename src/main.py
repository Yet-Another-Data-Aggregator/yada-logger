import os
import sys
import time
import importlib
import threading
import json

import config
import network
from channel_manager import ChannelManager
from config import Config
from file_utils import Files
import file_utils


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


def scan_run():
    """
    Main loop of the application. Runs all channels, sleeps until next channel run time, and checks for channel
    updates if the interval is up.
    """

    # Run all channels and then sleep until the next channel should run
    while running:
        wait_time, results, faults = ChannelManager.run_channels()

        time.sleep(wait_time)


def network_run():
    now = time.time()

    while running:
        time.sleep(5)

        if not should_upload or Files.is_directory_empty(file_utils.upload_directory):
            continue

        with Files.get_most_recent_file_blocking(file_utils.upload_directory) as upload_file:
            datastore.upload_data(list(map(json.loads, upload_file.readlines())))
            Files.delete(upload_file)

        #if should_upload and faults:
        #    datastore.upload_faults(faults)

        if time.time() - now > template_update_interval:
            now = time.time()
            check_update()


if __name__ == '__main__':
    initialize()

    scanThread = threading.Thread(target=scan_run)
    networkThread = threading.Thread(target=network_run)

    scanThread.start()
    networkThread.start()

    while running:
        time.sleep(15 * 60)

    scanThread.stop()
    networkThread.stop()

    # Restart the process if True
    if restart:
        os.execv(sys.executable, ['python'] + sys.argv)
