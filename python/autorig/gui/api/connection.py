import autorig.gui.qt.QtGui as _qt
import autorig.gui.qt.QtCore as _qtcore


class Connection(_qt.QGraphicsPathItem):
    """A connection between to attributes."""

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self.source = self.destination = None
        self._source_pos = self._destination_pos = _qtcore.Qt.QPointF(0, 0)

    def paint(self, painter, option, widget):
        """Draw a path between the source and destination `Attribute`."""
        self.setZValue(-1)
        if self.source and not self.destination:
            # Draw to the mouse cursor.
            pass
        super(Connection, self).paint(painter, option, widget)

    @property
    def source_pos(self):
        """Return the current source position of the `Connection`.

        :rtype: Qt.QPointF
        """
        return self._source_pos

    @source_pos.setter
    def source_pos(self, pos):
        """Set the start position, from the source attribute.

        :param pos: Start position.
        :type pos: tuple(float, float) or Qt.QPointF
        """
        if not isinstance(pos, _qtcore.Qt.QPointF):
            pos = _qtcore.Qt.QPointF(pos[0], pos[1])
        path = _qt.QPainterPath()
        path.quadTo(pos, self.destination_pos)
        self._source_pos = pos
        self.setPath(path)

    @property
    def destination_pos(self):
        """Return the current destination position of the `Connection`.

        :rtype: Qt.QPointF
        """
        return self._destination_pos

    @destination_pos.setter
    def destination_pos(self, pos):
        """Set the end position, from the source attribute.

        :param pos: End position.
        :type pos: tuple(float, float) or Qt.QPointF
        """
        if not isinstance(pos, _qtcore.Qt.QPointF):
            pos = _qtcore.Qt.QPointF(pos[0], pos[1])
        path = _qt.QPainterPath()
        path.quadTo(self.source_pos, pos)
        self._destination_pos = pos
        self.setPath(path)
