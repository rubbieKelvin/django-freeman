class DotDict(dict):
    """A custom dictionary that allows accessing and setting properties with the dot notation."""

    def __getattr__(self, key):
        """Return the value of the given key as an attribute."""
        try:
            value = self[key]
        except KeyError:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{key}'")
        if isinstance(value, dict):
            return DotDict(value)
        return value

    def __setattr__(self, key, value):
        """Set the value of the given key as an attribute."""
        self[key] = value
