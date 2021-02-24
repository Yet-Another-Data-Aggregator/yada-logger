import configparser
import sys

# Location of the configuration file
CONFIG_FILE = "config.ini"


def parse_config_file(filename):
    """
    Parses the configuration file with the given filename.

    :param filename: The filename of the configuration file
    :return: The configuration object created from the file
    """
    config = configparser.ConfigParser()
    config.read(filename)

    return config


def section(key):
    """
    Decorator to inject config section with the given key into the decorated function. If the section is not found
    the function will not be called.

    :param key: The section of the config object associated with the given key
    :return: The decorated function
    """

    def decorator(function):
        def wrapped():
            if key in Config.config:
                function(Config.config[key])

        return wrapped

    return decorator


class Config:
    """
    Static utility class to help manage the application configuration.
    """

    # The configuration object
    config = parse_config_file(CONFIG_FILE)

    @staticmethod
    def get():
        """
        Returns a reference to the configuration object.
        :return: The config object
        """
        return Config.config

    @staticmethod
    def write_changes():
        """
        Writes any changes to the configuration file.

        :return:
        """
        with open(CONFIG_FILE, "w") as file:
            Config.config.write(file)

    @staticmethod
    def required(section, key, message=""):
        """
        Returns the configuration value for the given key or else exists the application with the given error message.

        :param section: The section to find the key in.
        :param key: The key associated with the value.
        :param message: The message to exit the system with.
        :return: The value associated with the given key in the given configuration object.
        """
        if key not in section:
            sys.exit(message)
        return section[key]
