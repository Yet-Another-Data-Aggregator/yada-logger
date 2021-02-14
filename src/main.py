import os
import sys
import time

from config import Config
import file_utils
import network
from channel_manager import ChannelManager

template_refresh_interval = 60 * 5

restart = False
running = True


def initialize():
    global template_refresh_interval

    config = Config.get()

    if "config" in config:
        template_refresh_interval = float(config["config"].get("template_refresh_interval", 60 * 5))

    network.initialize()
    file_utils.initialize()
    ChannelManager.initialize()

    if network.should_update_template():
        network.fetch()

    ChannelManager.load_from_config(config)


def check_update():
    if not network.should_update_template():
        return

    network.fetch()

    global running, restart
    running = False
    restart = True


def run():
    now = time.time()

    # Run all channels and then sleep until the next channel should run
    while running:
        wait_time = ChannelManager.run_channels()

        time.sleep(wait_time)

        if time.time() - now > template_refresh_interval:
            now = time.time()
            check_update()


if __name__ == '__main__':
    initialize()

    run()

    # Restart the process if True
    if restart:
        os.execv(sys.executable, ['python'] + sys.argv)
