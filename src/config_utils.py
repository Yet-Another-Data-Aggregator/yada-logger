import sys


def required(config, key, message=""):
    """
    Returns the configuration value for the given key or else exists the application with the given error message.

    :param config: The configuration object to get the value from.
    :param key: The key associated with the value.
    :param message: The message to exit the system with.
    :return: The value associated with the given key in the given configuration object.
    """
    if key not in config:
        sys.exit(message)
    return config[key]