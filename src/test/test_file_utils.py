from pathlib import Path
from datetime import datetime

import src.file_utils as file_utils


class TestFileUtils:
    filename = "test_file"

    def test_get_file_return_is_not_none(self, tmp_path):
        assert file_utils.get_file(tmp_path, self.filename) is not None

    def test_get_file_return_is_a_path(self, tmp_path):
        assert isinstance(file_utils.get_file(tmp_path, self.filename), Path)

    def test_get_file_is_in_correct_directory(self, tmp_path):
        assert file_utils.get_file(tmp_path, self.filename).parent == tmp_path

    def test_get_file_returns_new_file(self, tmp_path):
        assert file_utils.get_file(tmp_path, self.filename).exists() is False

    def test_get_file_returns_file_with_correct_prefix(self, tmp_path):
        assert file_utils.get_file(tmp_path, self.filename).name.startswith("log_")

    def test_get_file_returns_file_if_it_exists(self, tmp_path):
        test_text = "Hello World"

        expected_file = tmp_path.joinpath("log_1-1-2021-00:00:00_test_file.log")
        expected_file.write_text(test_text)

        test_file = file_utils.get_file(tmp_path, self.filename)

        assert expected_file == test_file
        assert expected_file.read_text() == test_text

    def test_get_file_returns_smaller_file(self, tmp_path):
        kilobyte_filepath = tmp_path.joinpath("log_1-1-2021-00:00:00_test_file.log")
        with kilobyte_filepath.open(mode="w+") as file:
            file.seek(1024)
            file.write('\0')

        assert file_utils.get_file(tmp_path, self.filename, 512) != kilobyte_filepath

    def test_get_file_returns_more_recent_file(self, tmp_path):
        old_file = tmp_path.joinpath("log_1-1-2021-00:00:00_test_file.log")
        old_file.write_text("hello")

        new_file = tmp_path.joinpath("log_2-1-2021-00:00:00_test_file.log")
        new_file.write_text("hello2")

        assert file_utils.get_file(tmp_path, self.filename) == new_file
        assert file_utils.get_file(tmp_path, self.filename).read_text() == "hello2"

    def test_get_datetime_from_filename(self):
        date_string = "1-1-2021-00:00:00"
        filename = "log_" + date_string + "_test_file.txt"
        assert file_utils.get_datetime_from_filename(filename) == datetime.strptime(date_string, "%m-%d-%Y-%H:%M:%S")
