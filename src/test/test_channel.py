from unittest import TestCase

from src.channel import Channel


class IntChannel(Channel):
    def scan(self):
        return {"integer": 1}


class TestChannel(TestCase):
    def test_scan_value_is_not_null(self):
        date_channel = IntChannel("test_int_channel", "int", 5)
        channel_value = date_channel.scan()

        return channel_value is not None and len(channel_value.keys()) == 1

    def test_scan_value_is_correct(self):
        date_channel = IntChannel("test_int_channel", "int", 5)
        channel_value = date_channel.scan()

        return channel_value["integer"] == 1
