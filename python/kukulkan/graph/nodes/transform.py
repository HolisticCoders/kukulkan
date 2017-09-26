from kukulkan.graph.api import Node
from kukulkan.graph.attributes.matrix import XForm


class Transform(Node):
    """A transformation node."""

    builtin_attributes = {
        'xform': XForm,
    }

    def translation(self):
        """Return the translations of this node."""
        matrix = self.get()
        return matrix[0][3], matrix[1][3], matrix[2][3]

    def rotation(self):
        """Return the rotation of this node."""
        matrix = self.get()
        return matrix[0][3], matrix[1][3], matrix[2][3]

    def scale(self):
        """Return the scale of this node."""
        matrix = self.get()
        return matrix[0][0], matrix[1][1], matrix[2][2]
