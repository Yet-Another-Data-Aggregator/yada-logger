import configparser
import os
import sys
import time

import network
import file_utils
from channel_manager import ChannelManager

CONFIG_FILE = "config.ini"
FIVE_MINUTES = 60 * 5

restart = False
running = True


def run():
    now = time.time()

    while running:
        wait_time = ChannelManager.run_channels()

        time.sleep(wait_time)

        if time.time() - now > FIVE_MINUTES:
            now = time.time()
            # TODO Check for new template definitions
            pass


if __name__ == '__main__':
    print("Hello")

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    network.initialize(config)
    file_utils.initialize(config)
    ChannelManager.initialize(config)

    ChannelManager.load_from_config(config)


    #network.fetch_channels()

    #print(network.should_update_template())

    run()

    # Restart the process if True
    if restart:
        os.execv(sys.executable, ['python'] + sys.argv)
