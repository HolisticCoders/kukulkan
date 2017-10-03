import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.qt.QtCore as _qtcore


class BaseConnection(_qt.QGraphicsPathItem):
    """A connectin object.

    This class handles basic mechanics of connections, like
    path drawing, thickness, etc...
    """

    def __init__(self, *args, **kwargs):
        super(BaseConnection, self).__init__(*args, **kwargs)
        self.setZValue(-3)
        self.stroker = _qt.QPainterPathStroker()
        self.stroker.setWidth(5)
        self.stroker.setCapStyle(_qtcore.Qt.RoundCap)
        self.source_pos = self.destination_pos = _qtcore.QPointF(0, 0)
        self.flat_brush = _qt.QBrush(_qt.QColor(73, 73, 73))

    def compute_path(self):
        """Compute the path of this connection.

        The computed path will be drawn between the source_pos and
        destination_pos of this connection.

        This method requires `BaseConnection.source_pos` and
        `BaseConnection.destination_pos` attributes to be set.
        Both must be `PySide.QtCore.QPointF` attributes or present
        a similar interface (`PySide.QtCore.QPointF.x` and
        `PySide.QtCore.QPointF.y` are used in particular).
        """
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

        stroker = _qt.QPainterPathStroker()
        stroker.setWidth(5)
        stroker.setCapStyle(_qtcore.Qt.RoundCap)

        self.setPath(stroker.createStroke(path))

    def paint(self, painter, option, widget):
        """Draw a path between the source and destination `Attribute`."""
        self.compute_path()
        super(BaseConnection, self).paint(painter, option, widget)
        painter.fillPath(self.path(), self.flat_brush)


class PendingConnection(BaseConnection):
    """A `Connection` not yet connected between two `Plug` objects.

    This is used when a user begins to drag a `Connection` between
    two `Plug` objects.
    """

    def __init__(self, source, owner):
        super(PendingConnection, self).__init__()
        self.source = source
        self.owner = owner
        self.setParentItem(source)
        self.source_pos = source.boundingRect().center()

    def update_path(self, mouse_event):
        """Update the path of this connection.

        The path is updated by plugs asking for this `PendingConnection`.

        :param mouse_event: Event triggering the update. This is passed
                            by the owner `Plug` in its mouseMoveEvent.
        :type mouse_event:
        """
        if not self.source:
            return
        self.source_pos = self.source.boundingRect().center()
        self.destination_pos = self.owner.mapToItem(
            self.source,
            mouse_event.pos(),
        )
        self.compute_path()


class Connection(BaseConnection):
    """A connection between to attributes."""

    def __init__(self, source, destination):
        super(Connection, self).__init__()
        self.source = source
        self.destination = destination
        source.connections[str(destination)] = self
        destination.connections[str(source)] = self

    def compute_path(self):
        """Update the path of this connection.

        It will be drawn between the source and destination Attributes.
        If there is no destination attribute, the mouse cursor position
        will be used instead.
        """
        if self.source:
            self.source_pos = self.source.boundingRect().center()
        if self.destination:
            self.destination_pos = self.destination.mapToItem(
                self.source,
                self.destination.boundingRect().center(),
            )
        super(Connection, self).compute_path()
