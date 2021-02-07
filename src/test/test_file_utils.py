from src.file_utils import *

import os


class TestFileUtils:
    def test_get_file_return_is_not_none(self):
        assert get_file() is not None

    def test_get_file_return_is_a_file(self, tmp_path):
        print(tmp_path)
        assert True
