from src.channel import Channel

ONE_MINUTE = 60
FIVE_MINUTES = 60 * 5


class IntChannel(Channel):
    def scan(self):
        return {"integer": 1}


class CounterChannel(Channel):
    def __init__(self, name, class_name, cache_size):
        super().__init__(name, class_name, cache_size)
        self.counter = 0

    def scan(self):
        self.counter += 1
        return self.counter


class LogIntervalChannel(Channel):
    def __init__(self, name, channel_type, cache_size):
        super().__init__(name, channel_type, cache_size)
        self.test_switch = True

    def next_log_interval(self):
        if self.test_switch:
            self.test_switch = False
            return FIVE_MINUTES
        else:
            return ONE_MINUTE

    def scan(self):
        return {"integer": 1}


class FaultChannel(Channel):
    def scan(self):
        return {"integer": 1}, ["Fault one", "Fault two"]


class ExceptionChannel(Channel):
    def scan(self):
        raise Exception("Test Exception has occurred")


class TestChannel:
    def test_scan_value_is_not_null(self):
        test_channel = IntChannel("test_channel", "IntChannel", 5)

        channel_value = test_channel.scan()

        assert channel_value is not None and len(channel_value.keys()) == 1

    def test_scan_value_is_correct(self):
        test_channel = IntChannel("test_channel", "IntChannel", 5)

        channel_value = test_channel.scan()

        assert channel_value["integer"] == 1

    def test_next_log_interval_returns_correct_time(self):
        channel = LogIntervalChannel("test_channel", "LogIntervalChannel", 5)

        assert channel.next_log_interval() == FIVE_MINUTES

    def test_next_log_interval_returns_more_than_once(self):
        test_channel = LogIntervalChannel("test_channel", "LogIntervalChannel", 5)

        test_channel.next_log_interval()

        assert test_channel.next_log_interval() == ONE_MINUTE

    def test_next_log_interval_can_return_different_values(self):
        test_channel = LogIntervalChannel("test_channel", "LogIntervalChannel", 5)

        first_interval = test_channel.next_log_interval()
        second_interval = test_channel.next_log_interval()

        assert first_interval == FIVE_MINUTES and second_interval == ONE_MINUTE

    def test_cache_empty_on_first_run(self):
        channel = IntChannel("test_channel", "IntChannel", 5)
        assert channel.cache == []

    def test_cache_size_0_does_not_throw_error(self):
        channel = IntChannel("test_channel", "IntChannel", 0)
        channel.log()

        assert channel.cache == []

    def test_cache_with_one_value(self):
        channel = CounterChannel("test_channel", "CounterChannel", 1)
        channel.log()

        assert channel.cache == [1]

        channel.log()

        assert channel.cache == [2]

    def test_cache_larger_than_one(self):
        channel = CounterChannel("test_channel", "CounterChannel", 2)
        channel.log()
        channel.log()

        assert channel.cache == [2, 1]

        channel.log()

        assert channel.cache == [3, 2]

    def test_scan_fault_tuple(self):
        channel = FaultChannel("test_channel", "FaultChannel", 0)
        value, faults = channel.log()

        assert len(faults) == 2
        assert faults[0] == "Fault one"
        assert faults[1] == "Fault two"
        assert value == {"integer": 1}

    def test_exception_returns_fault(self):
        channel = ExceptionChannel("test_channel", "ExceptionChannel", 0)
        value, faults = channel.log()

        assert value == {}
        assert len(faults) == 1
        assert faults[0] == "Exception('Test Exception has occurred')"
