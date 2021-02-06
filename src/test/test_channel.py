from unittest import TestCase

from src.channel import Channel


one_minute = 1000 * 60
five_minutes = 1000 * 60 * 5


class IntChannel(Channel):
    def scan(self):
        return {"integer": 1}


class LogIntervalChannel(Channel):
    def __init__(self, name, channel_type, read_rate):
        super().__init__(name, channel_type, read_rate)
        self.test_switch = True

    def next_log_interval(self):
        if self.test_switch:
            self.test_switch = False
            yield five_minutes
        else:
            yield one_minute

    def scan(self):
        return {"integer": 1}


class TestChannel(TestCase):
    def test_scan_value_is_not_null(self):
        test_channel = IntChannel("test_int_channel", "int", 5)

        channel_value = test_channel.scan()

        return channel_value is not None and len(channel_value.keys()) == 1

    def test_scan_value_is_correct(self):
        test_channel = IntChannel("test_int_channel", "int", 5)

        channel_value = test_channel.scan()

        return channel_value["integer"] == 1

    def test_next_log_interval_returns_correct_time(self):
        test_channel = LogIntervalChannel("test_int_channel", "int", 5)

        return test_channel.next_log_interval() == five_minutes

    def test_next_log_interval_returns_more_than_once(self):
        test_channel = LogIntervalChannel("test_int_channel", "int", 5)

        test_channel.next_log_interval()

        return test_channel.next_log_interval() == five_minutes

    def test_next_log_interval_can_return_different_values(self):
        test_channel = LogIntervalChannel("test_int_channel", "int", 5)

        first_interval = test_channel.next_log_interval()
        second_interval = test_channel.next_log_interval()

        return first_interval == five_minutes and second_interval == one_minute
