class Channel:
    """Channel represents the logic that converts sensor data into a logged value."""

    def __init__(self, name, class_name, cache_size):
        """Channel initializer. Sets the name, cache size, and initializes the cache to an empty list."""
        self.name = name
        self.cache_size = cache_size
        self.class_name = class_name
        self.cache = []

    @classmethod
    def from_config(cls, config):
        """Returns a new channel object from config."""
        return cls(
            config.name.replace("channel/", ""),
            config.class_name,
            int(config.get("cache_size", 0))
        )

    def __repr__(self):
        return f"Channel[name: {self.name}, cache_size: {self.cache_size}, cache: {self.cache}]"

    def write_to_config(self, config):
        """Writes the current channel to the given config."""
        config[f"channel/{self.name}"] = {
            "cache_size": self.cache_size,
            "class_name": self.class_name
        }

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
        """Runs scan and adds value to cache"""
        try:
            value = self.scan()

            # Add value to cache and pop if cache has reached max size
            if self.cache_size > 0:
                if len(self.cache) >= self.cache_size:
                    self.cache.pop()
                self.cache.insert(0, value)

            return value
        except Exception as e:
            return {}, [repr(e)]
