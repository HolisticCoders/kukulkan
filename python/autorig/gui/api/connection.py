import autorig.gui.qt.QtGui as _qt
import autorig.gui.qt.QtCore as _qtcore


class Connection(_qt.QGraphicsPathItem):
    """A connection between to attributes."""

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self.source = self.destination = None

    def paint(self, painter, option, widget):
        """Draw a path between the source and destination `Attribute`."""
        if self.source and not self.destination:
            # Draw to the mouse cursor.

    def update_connection(self):
        """"""
