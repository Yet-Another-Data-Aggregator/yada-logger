import os
import sys
import time

import config
import network
from network import Network
from channel_manager import ChannelManager
from config import Config
from file_utils import Files

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
    global template_update_interval
    template_update_interval = float(section.get("template_refresh_interval", 60 * 5))


def initialize():
    """
    Initializes the application and checks if the channels need updated.
    """
    load_variables()

    Network.initialize()
    Files.initialize()
    ChannelManager.initialize()

    if Network.should_update_template():
        Network.fetch()

    ChannelManager.load_from_config(Config.get())


def check_update():
    """
    Checks whether the channels need updating. If not, this function returns without doing anything, if so, the new
    channels are fetched and the running and restart variables are set to reload the application.
    """
    if not Network.should_update_template():
        return

    Network.fetch()

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
        wait_time = ChannelManager.run_channels()

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
