import autorig.gui.qt.QtGui as _qt
import autorig.gui.qt.QtCore as _qtcore


class Connection(_qt.QGraphicsPathItem):
    """A connection between to attributes."""

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self.is_pending = True
        self.source = self.destination = None
        self.source_pos = self.destination_pos = _qtcore.QPointF(0, 0)
        self.mouse_cursor_pos = _qtcore.QPointF(0, 0)

    def paint(self, painter, option, widget):
        """Draw a path between the source and destination `Attribute`."""
        self.setZValue(-1)
        super(Connection, self).paint(painter, option, widget)

    def update_path(self, event=None):
        """Update the path of this connection.

        It will be drawn between the source and destination Attributes.
        If there is no destination attribute, the mouse cursor position
        will be used instead.

        :param event: Mouse event triggering this update.
        """
        if self.source:
            self.source_pos = self.source.boundingRect().center()
        elif event:
            self.source_pos = event.pos()
        if self.destination:
            self.destination_pos = self.destination.boundingRect().center()
        elif event:
            self.destination_pos = event.pos()

        path = _qt.QPainterPath()
        path.moveTo(self.source_pos)

        control_x = self.destination_pos.x() - self.source_pos.x()
        control_y = self.destination_pos.y() - self.source_pos.y()

        control_source = _qtcore.QPointF(
            self.source_pos.x() + control_x * .4,
            self.source_pos.y() + control_y * 0,
        )

        control_destination = _qtcore.QPointF(
            self.source_pos.x() + control_x * .6,
            self.source_pos.y() + control_y * 1,
        )

        path.cubicTo(
            control_source,
            control_destination,
            self.destination_pos,
        )

        self.setPath(path)

    def paint(self, painter, option, widget):
        if not self.is_pending:
            self.update_path()
            print 'has updated'
        super(Connection, self).paint(painter, option, widget)