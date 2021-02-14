import configparser
import sys

CONFIG_FILE = "config.ini"


def parse_config_file(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    return config


class Config:
    config = parse_config_file(CONFIG_FILE)

    @staticmethod
    def get():
        return Config.config

    @staticmethod
    def write_changes():
        with open(CONFIG_FILE, "w") as file:
            Config.config.write(file)

    @staticmethod
    def required(section, key, message=""):
        """
        Returns the configuration value for the given key or else exists the application with the given error message.

        :param key: The key associated with the value.
        :param message: The message to exit the system with.
        :return: The value associated with the given key in the given configuration object.
        """
        if key not in section:
            sys.exit(message)
        return section[key]
