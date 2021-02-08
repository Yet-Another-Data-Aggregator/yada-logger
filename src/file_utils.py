from pathlib import Path

from datetime import datetime

logging_directory = Path("logs/")

upload_file_prefix = "upload_"
upload_file_max_size = 10 * 1024

log_file_prefix = "log_"
log_file_max_size = 100 * 1024

date_format = "%m-%d-%Y-%H:%M:%S"


def log_value(value_dict):
    pass


def get_file(directory, filename, max_file_size=log_file_max_size, file_prefix=log_file_prefix):
    """Returns the file in the given directory that is the most recently created whose size is less than the given
    maximum size."""

    files = list(directory.iterdir())
    file_num = len(files)

    # Check if most recently created file is less than the maximum size.
    if file_num > 0:
        most_recent_file = sorted(
            files,
            key=lambda dir_file: get_datetime_from_filename(dir_file.name),
            reverse=True
        )[0]

        if most_recent_file.stat().st_size < max_file_size:
            return most_recent_file

    # No file found, return a new one.
    return directory.joinpath(f"{file_prefix}{get_datetime()}{filename}.log")


def get_datetime():
    """Gets the current time with a standard date format"""
    return datetime.now().strftime(date_format)


def get_datetime_from_filename(filename):
    """Returns a datetime object from the given filename. The datetime must be in %m-%d-%Y-%H:%M:%S format and must
    be between the first and second underscore '_' in the filename."""
    start = filename.find('_') + 1
    end = filename.find('_', start)

    date_string = filename[start:end]

    return datetime.strptime(date_string, date_format)
