import autorig.gui.qt.QtGui as _qt
import autorig.gui.qt.QtCore as _qtcore
import autorig.gui.api.connection as _conn


class Plug(_qt.QGraphicsItem):
    """An `Attribute` plug, a handle to set or get the `Attribute`."""

    plug_types = [
        'input',
        'output',
    ]
    plug_type = None
    _max_connections = {
        'input': 1,
        'output': None,
    }

    def __init__(self, attribute, *args, **kwargs):
        # Gotta make sure we don't have a weird kind of plug type.
        if self.plug_type not in self.plug_types:
            error = ' '.join([
                'Wrong type of plug.',
                'Found: {}.'.format(self.plug_type),
                'Should be one of input or output.',
            ])
            raise TypeError(error)
        self.attribute = attribute

        super(Plug, self).__init__(*args, **kwargs)

        self.connections = {}
        self.pending_connection = None
        self.setParentItem(self.attribute)
        self.reset()

    def __str__(self):
        return '.'.join([str(self.attribute), self.plug_type])

    def reset(self):
        """Reset the graphic state to its initial value."""
        self.x = 0
        self.y = 0
        self.inner_color = _qt.QColor(53, 53, 53)
        self.background = _qt.QBrush(_qt.QColor(200, 180, 150))
        self.outline = _qt.QPen(_qt.QColor(23, 23, 23))

    @property
    def node(self):
        """Return the `Node` this `Plug` belongs to.

        :rtype: Node
        """
        return self.attribute.node

    @property
    def max_connections(self):
        """Return the maximum number of connections for this `Plug`.

        If no maximum is set, return `None`.

        :rtype: int or None
        """
        return self._max_connections[self.plug_type]

    def boundingRect(self):
        return _qtcore.QRectF(
            self.x,
            self.y,
            self.attribute.size,
            self.attribute.size,
        )

    def paint(self, painter, option, widget):
        painter.setBrush(self.background)
        painter.setPen(self.outline)
        painter.drawEllipse(
            self.x,
            self.y,
            self.attribute.size,
            self.attribute.size,
        )

    def mousePressEvent(self, event):
        """Initiate a `Connection` from this `Attribute`."""
        if event.button() != _qtcore.Qt.MouseButton.LeftButton:
            return
        if self.pending_connection:
            return

        if self.max_connections is not None:
            # Meaning there is an actual number of maximum connections
            # possible.
            # Usually means this is an input plug, which can only have
            # one connection, that drives it.
            if len(self.connections) >= self.max_connections:
                return

        self.pending_connection = _conn.Connection()
        self.pending_connection.setParentItem(self)
        self.pending_connection.source = self
        self.pending_connection.source_pos = self.boundingRect().center()

    def mouseMoveEvent(self, event):
        """Update the `Connection` path."""
        if not self.pending_connection:
            return
        self.pending_connection.update_path(event)

    def mouseReleaseEvent(self, event):
        """Connect the `Attribute` or remove the pending `Connection`."""
        if not self.pending_connection:
            return
        scene = self.scene()
        destination = scene.itemAt(event.scenePos())
        if not isinstance(destination, Plug):
            self._delete_pending_connection()
        elif str(destination) in self.connections:
            self._delete_pending_connection()
        else:
            self.pending_connection.destination = destination
            self.connections[str(destination)] = self.pending_connection
            self.attribute.connections[str(destination)] = self.pending_connection
            self.node.connections[str(destination)] = self.pending_connection
            destination.connections[str(destination)] = self.pending_connection
            destination.attribute.connections[str(destination)] = self.pending_connection
            destination.node.connections[str(destination)] = self.pending_connection
            self.pending_connection.is_pending = False
            self.pending_connection = None

    def _delete_pending_connection(self):
        """Remove the pending connection.

        Can be called if node valid `Attribute` was found to connect to.
        """
        if not self.pending_connection:
            return
        if self.pending_connection not in self.scene().items():
            return
        self.scene().removeItem(self.pending_connection)
        self.pending_connection = None


class Input(Plug):
    """An input `Plug`."""
    plug_type = 'input'


class Output(Plug):
    """An output `Plug`."""
    plug_type = 'output'
