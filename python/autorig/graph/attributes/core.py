from autorig.graph.api import Attribute


class String(Attribute):
    """A string attribute."""

    def validate_value(self, value):
        """Make sure we end-up with a string.

        :rtype: str
        """
        return str(value)


class Float(Attribute):
    """A float attribute."""

    def validate_value(self, value):
        """Make sure we end-up with a float.

        :rtype: float
        """
        return float(value)


class Integer(Attribute):
    """A integer attribute."""

    def validate_value(self, value):
        """Make sure we end-up with an integer.

        :rtype: int
        """
        return int(value)
