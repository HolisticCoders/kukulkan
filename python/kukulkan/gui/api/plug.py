import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.qt.QtCore as _qtcore
import kukulkan.gui.api.connection as _conn


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

        source = self
        if self.plug_type == 'input' and self.connections:
            # Disconnect the `Connection` from this plug.
            key, conn = self.connections.popitem()
            conn.source.connections.pop(str(self))
            if conn in self.scene().items():
                self.scene().removeItem(conn)
            source = conn.source
        self.create_pending_connection(source)
        self.pending_connection.update_path(event)

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
        owner = self.pending_connection.source
        under_cursor = scene.items(event.scenePos())
        plugs = [item for item in under_cursor if isinstance(item, Plug)]
        if plugs:
            to = plugs[0]
            if owner.plug_type == 'output':
                source = owner
                destination = to
            else:
                source = to
                destination = owner
            source.connect(destination)
        self._delete_pending_connection()

    def create_pending_connection(self, source=None):
        """Create a `PendingConnection` and return it.

        If there is already a pending connection, return it.

        You can specify another sourceplug with the ``source`` argument,
        making the PendingConnection start from another spot.

        :param source: Source plug of this PendingConnection.
        :type source: Plug
        :rtype: PendingConnection
        """
        if self.pending_connection:
            return self.pending_connection
        if source is None:
            source = self
        self.pending_connection = _conn.PendingConnection(source, self)
        self.grabMouse()
        return self.pending_connection

    def remove_connection(self, key):
        """Remove a specific connection, by key.

        A connection key is formatted as follows:

            ``node_name.attribute_name.plug_type``

        :param str key: Name of the connection to remove.
        """
        conn = self.connections.pop(key)
        conn.source.connections.pop(str(conn.destination), None)
        conn.destination.connections.pop(str(conn.source), None)
        if conn in self.scene().items():
            self.scene().removeItem(conn)
        self.on_disconnection(other)
        other.on_disconnection(self)

    def disconnect(self, other):
        """Remove the connection between this `Plug` and ``other``

        :param other: `Plug` to connect to.
        :type other: Plug
        """
        # Find a common connection
        other_connections = other.connections.values()
        for key, conn in self.connections.iteritems():
            if conn not in other_connections:
                continue
            conn.source.connections.pop(str(conn.destination), None)
            conn.destination.connections.pop(str(conn.source), None)
            if conn in self.scene().items():
                self.scene().removeItem(conn)
            self.on_disconnection(other)
            other.on_disconnection(self)
            return

    def connect(self, other):
        """Create a connection between this plug and another one.

        :param other: `Plug` to connect to.
        :type other: Plug
        :return: The resulting connection.
        :rtype: Connection
        """
        if self.plug_type == 'input':
            source = other
            destination = self
        elif self.plug_type == 'output':
            source = self
            destination = other
        if not self._validate_connection(source, destination):
            return
        return _conn.Connection(source, destination)

    def on_connection(self, other):
        """Method called when this `Plug` gets connected.

        :param other: Other `Plug` connected to this one.
        :type other: Plug
        """

    def on_disconnection(self, other):
        """Method called when this `Plug` gets disconnected.

        :param other: Other `Plug` disconnected from this one.
        :type other: Plug
        """

    @staticmethod
    def _validate_connection(source, destination):
        """Return `True` if the connection can proceed.

        Basically, a connection is invalid if:

            * There is no source or destination;
            * The destination is not a `Plug`;
            * The destination is already connected;
            * The source and destination are both inputs or outputs;

        :param source: Source of the connection.
        :param destination: Destination of the connection.
        :type source: Plug
        :type destination: Plug
        :rtype: bool
        """
        if not source:
            return False
        if not destination:
            return None
        if not isinstance(destination, Plug):
            return False
        if destination.connections:
            return False
        if source.plug_type == destination.plug_type:
            return False
        return True

    def _delete_pending_connection(self):
        """Remove the pending connection.

        Can be called if node valid `Attribute` was found to connect to.
        """
        if not self.pending_connection:
            return
        source = self.pending_connection.source
        key = str(self.pending_connection)
        source.connections.pop(key, None)
        if self.pending_connection in self.scene().items():
            self.scene().removeItem(self.pending_connection)
        self.pending_connection = None
        self.ungrabMouse()


class Input(Plug):
    """An input `Plug`."""
    plug_type = 'input'


class Output(Plug):
    """An output `Plug`."""
    plug_type = 'output'
