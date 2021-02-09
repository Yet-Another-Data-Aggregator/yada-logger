import configparser
import time

import channel_manager

CONFIG_FILE = "config.ini"
FIVE_MINUTES_IN_SECONDS = 60 + 5

restart = False
running = True


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    channel_manager.load_from_config(config)

    now = time.time()

    while running:
        wait_time = channel_manager.run_channels()

        time.sleep(wait_time)

        if time.time() - now > FIVE_MINUTES_IN_SECONDS:
            # TODO Check for new template definitions
            pass

    if restart:
        # TODO close and restart script
        pass
