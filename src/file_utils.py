import os
from datetime import datetime
from pathlib import Path
import threading
import time

import config

# The path to the directory where logs are saved
logging_directory = Path("logs/")

# The path to the directory where upload files are saved
value_upload_directory = Path("upload/")

# The path to the directory where upload files for faults are save
fault_upload_directory = Path("fault_upload/")

# The prefix of files that are pending upload
upload_file_prefix = "upload_"

# Prefix of log files
log_file_prefix = "log_"

# Maximum size of log files
max_file_size = 100 * 1024

# Format of date to use in filenames
date_format = "%m-%d-%Y-%H:%M:%S"

# A dictionary of open files for locking
open_files = set()

# For locking critical file operations
lock = threading.Lock()


@config.section("storage")
def load_variables(section):
    """
    Loads variables from the "storage" section of the configuration file

    :param section: The config section
    """
    global logging_directory, upload_file_prefix, log_file_prefix, date_format, max_file_size, fault_upload_directory
    global value_upload_directory

    logging_directory = Path(section.get("logging_directory", "logs/"))
    value_upload_directory = Path(section.get("value_upload_directory", "upload/"))
    fault_upload_directory = Path(section.get("fault_upload_directory", "fault_upload/"))
    upload_file_prefix = section.get("upload_file_prefix", "upload_")
    log_file_prefix = section.get("log_file_prefix", "log_")
    max_file_size = int(section.get("max_file_size", 100 * 1024))
    date_format = section.get("date_format", "%m-%d-%Y-%H:%M:%S")


class Files:
    """
    Utility class to manage files for the application.
    """

    @staticmethod
    def initialize():
        """
        Load global variables from config.
        """
        load_variables()

    @staticmethod
    def directory_size():
        total = 0
        for dir_path, _, filenames in os.walk(logging_directory):
            for f in filenames:
                fp = os.path.join(dir_path, f)
                if not os.path.islink(fp):
                    total += os.path.getsize(fp)

            return total

    @staticmethod
    def get_append_log_file(directory, filename):
        """
        Returns a file in the given directory that is the most recently created whose size is less than the given
        maximum size.

        :param directory: The directory to get the file from. If this directory does not exist it will be created.
        :param filename: The name of the file after prefix and date.
        :return: A Path object representing the file.
        """
        lock.acquire()

        handle = Files.open(Files.get_append_file(directory, filename, log_file_prefix, "log"))

        lock.release()

        return handle

    @staticmethod
    def get_append_upload_file(directory, filename):
        lock.acquire()

        handle = Files.open(Files.get_append_file(directory, filename, upload_file_prefix, "upload"))

        lock.release()

        return handle

    @staticmethod
    def get_append_file(directory, filename, prefix, extension):
        if not directory.exists():
            directory.mkdir()

        most_recent_file = Files.get_most_recent_file(directory)

        if most_recent_file is not None and \
                most_recent_file.name not in open_files and \
                most_recent_file.stat().st_size < max_file_size:
            return most_recent_file

        # No file found, return a new one.
        return directory.joinpath(f"{prefix}{Files.get_datetime()}_{filename}.{extension}")

    @staticmethod
    def get_most_recent_file(directory):
        if not directory.exists():
            return None

        files = list(directory.iterdir())
        file_num = len(files)

        if file_num <= 0:
            return None

        return sorted(
            files,
            key=lambda dir_file: Files.get_datetime_from_filename(dir_file.name),
            reverse=True
         )[0]

    @staticmethod
    def get_most_recent_file_blocking(directory):
        lock.acquire()

        filepath = Files.get_most_recent_file(directory)

        lock.release()

        while True:
            lock.acquire()

            if filepath is not None and filepath.name not in open_files:
                handle = Files.open(filepath, mode="r")
                lock.release()
                return handle

            lock.release()

            time.sleep(1000)

    @staticmethod
    def is_directory_empty(directory):
        if not directory.exists():
            return True

        return len(list(directory.iterdir())) <= 0

    @staticmethod
    def open(filepath, mode="a"):
        open_files.add(filepath.name)
        return filepath.open(mode)

    @staticmethod
    def close(handle):
        lock.acquire()

        handle.close()
        open_files.remove(os.path.basename(handle.name))

        lock.release()

    @staticmethod
    def delete(handle):
        Files.close(handle)
        os.remove(handle.name)

    @staticmethod
    def get_datetime():
        """
        Gets a datetime object with the global date format.

        :return: The current datetime with the global format.
        """
        return datetime.now().strftime(date_format)

    @staticmethod
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
