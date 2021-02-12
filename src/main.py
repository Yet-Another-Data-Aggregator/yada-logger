import configparser
import time

from channel_manager import ChannelManager

CONFIG_FILE = "config.ini"
FIVE_MINUTES_IN_SECONDS = 60 + 5

restart = False
running = True


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    ChannelManager.initialize(config)
    ChannelManager.load_from_config(config)

    now = time.time()

    while running:
        wait_time = ChannelManager.run_channels()

        time.sleep(wait_time)

        if time.time() - now > FIVE_MINUTES_IN_SECONDS:
            now = time.time()
            # TODO Check for new template definitions
            pass

        test = False

    if restart:
        # TODO close and restart script
        pass
