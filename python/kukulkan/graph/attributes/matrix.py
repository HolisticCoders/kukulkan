from kukulkan.graph.api import Attribute


class Matrix(Attribute):
    """A matrix attribute."""

    shape = (4, 4)

    def validate_value(self, value):
        """Validate the shape of the specified matrix.

        :rtype: tuple(tuple)
        """
        err = '{v} cannot be converted to a {s} matrix !'
        if len(value) != self.shape[0]:
            raise ValueError(err.format(v=value, s=self.shape))
        for item in value:
            if len(item) != self.shape[1]:
                raise ValueError(err.format(v=value, s=self.shape))
        return value


class TypedMatrix(Matrix):
    """A Matrix with a predefined type of items."""

    def validate_item(self, item):
        """Implement that one to customize the items type.
        """
        raise NotImplementedError()

    def validate_value(self, value):
        """Make sure the content of the matrix fits the item type."""
        value = super(TypedMatrix, self).validate_value(value)
        for i, row in enumerate(value):
            value[i] = map(self.validate_item, row)
        return value


class XForm(TypedMatrix):
    """A 4 by 4 float `TypedMatrix`."""

    def validate_item(self, item):
        """Make sure we use `float` items."""
        return float(item)
