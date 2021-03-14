class Channel:
    """
    Channel represents the logic that converts sensor data into a logged value.
    """

    @classmethod
    def initialize(cls):
        """
        Creates a new class instance.

        :return: New class instance.
        """
        return cls()

    def __init__(self):
        """
        Channel initializer. Sets the cache size, and initializes the cache to an empty list.
        """
        self.cache_size = 0
        self.cache = []

    def __repr__(self):
        return f"Channel[name: {self.__class__.__name__}, cache_size: {self.cache_size}, cache: {self.cache}]"

    def next_log_interval(self):
        """
        Method that returns the time in seconds to wait until the next log.
        Default is 5 minutes.
        Can be a floating point number for milliseconds.
        """
        return 60 * 5

    def scan(self):
        """
        This method generates the actual value to be logged. The return type should be a dict with string keys and
        values that are serializable or a tuple containing the value dict and a list of any faults that were generated.
        Any exceptions that occur while this method is running will be caught and logged in place of a data value.
        """
        pass

    def log(self):
        """
        Runs scan and adds value to cache.
        """
        try:
            value = self.scan()

            # Add value to cache and pop oldest if cache has reached its max size
            if self.cache_size > 0:
                if len(self.cache) >= self.cache_size:
                    self.cache.pop()
                self.cache.insert(0, value)

            return value
        except Exception as e:
            return {}, repr(e)
