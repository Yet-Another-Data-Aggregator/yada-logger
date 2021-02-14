from datetime import datetime
from pathlib import Path

import config

# The path to the directory where logs are saved
logging_directory = Path("logs/")

# The prefix of files that are pending upload
upload_file_prefix = "upload_"

# Prefix of log files
log_file_prefix = "log_"

# Maximum size of log files
max_file_size = 100 * 1024

# Format of date to use in filenames
date_format = "%m-%d-%Y-%H:%M:%S"


@config.section("storage")
def load_variables(section):
    """
    Loads variables from the "storage" section of the configuration file

    :param section: The config section
    """
    global logging_directory, upload_file_prefix, log_file_prefix, max_file_size, date_format
    logging_directory = Path(section.get("logging_directory", "logs/"))
    upload_file_prefix = section.get("upload_file_prefix", "upload_")
    log_file_prefix = section.get("log_file_prefix", "log_")
    max_file_size = int(section.get("max_file_size", 100 * 1024))
    date_format = section.get("date_format", "%m-%d-%Y-%H:%M:%S")


def initialize():
    """
    Load global variables from config.
    """
    load_variables()


def get_file(directory, filename, file_size=max_file_size, file_prefix=log_file_prefix):
    """
    Returns a file in the given directory that is the most recently created whose size is less than the given
    maximum size.

    :param directory: The directory to get the file from. If this directory does not exist it will be created.
    :param filename: The name of the file after prefix and date.
    :param file_size: The maximum size a single file can be.
    :param file_prefix: A string to be prepended to the beginning of the file name.
    :return: A Path object representing the file.
    """
    files = list(directory.iterdir())
    file_num = len(files)

    # Check if most recently created file is less than the maximum size.
    if file_num > 0:
        most_recent_file = sorted(
            files,
            key=lambda dir_file: get_datetime_from_filename(dir_file.name),
            reverse=True
        )[0]

        if most_recent_file.stat().st_size < file_size:
            return most_recent_file

    # No file found, return a new one.
    return directory.joinpath(f"{file_prefix}{get_datetime()}{filename}.log")


def get_datetime():
    """
    Gets a datetime object with the global date format.

    :return: The current datetime with the global format.
    """
    return datetime.now().strftime(date_format)


def get_datetime_from_filename(filename):
    """
    Gets a datetime object from the given filename with the global date format.

    :param filename: The filename as a string get the date from.
    :return: A datetime object in the global date format.
    """
    # TODO make less brittle
    start = filename.find('_') + 1
    end = filename.find('_', start)

    date_string = filename[start:end]

    return datetime.strptime(date_string, date_format)
