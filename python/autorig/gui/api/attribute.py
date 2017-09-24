import autorig.gui.qt.QtGui as _qt
import autorig.gui.qt.QtCore as _qtcore
import autorig.gui.api.connection as _conn


class Attribute(_qt.QGraphicsItem):

    def __init__(self, name, node):
        super(Attribute, self).__init__(node)
        self.name = name
        self.node = node
        self._value = None
        self.connections = {}
        self.pending_connection = None
        self.reset()
        self.label_offset = 0
        self.is_output = False
        self.is_input = True

    def __str__(self):
        """Return the attribute string form."""
        return '.'.join(map(str, [self.node, self.name]))

    @property
    def plug_top_left_corner_x(self):
        """Return the top left corner of the plug to paint.

        This is required to allow an attribute to be either an
        input, or an output.

        :rtype: float
        """
        if self.is_output:
            return self.width - self.size * 1.5
        return self.x

    def reset(self):
        self.x = 0
        self.y = 0
        self.size = 10
        self.width = self.node.width + self.size

        self.label_font = _qt.QFont(
            'Helvetica [Cronyx]',
            10,
        )

        self.inner_color = _qt.QColor(53, 53, 53)
        self.outer_color = _qt.QColor(200, 180, 150)
        # self.border_color = _qt.QColor(20, 20, 20)
        # self.border_width = 10

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    # @value.getter
    # def value(self):
    #     pass


    def boundingRect(self):
        return _qtcore.QRectF(
            self.x,
            self.y,
            self.width,
            self.size,
        )

    def paint(self, painter, option, widget):
        painter.setPen(_qtcore.Qt.NoPen)
        # painter.setPen(self.border_color)
        # painter.pen().setWidth(self.border_width)

        self.paint_plug(painter, option, widget)
        self.paint_label(painter, option, widget)

    def paint_label(self, painter, option, widget):
        """Paint the label of the attribute, on the node."""
        painter.setFont(self.label_font)
        painter.setPen(self.node.label_color)
        painter.drawText(
            self.x + self.label_offset,
            self.y,
            self.width,
            self.size,
            _qtcore.Qt.AlignCenter,
            self.name,
        )

    def paint_plug(self, painter, option, widget):
        """Paint the source or destination plug."""
        # Paint the outer circle.
        painter.setBrush(_qt.QBrush(self.outer_color))
        painter.drawEllipse(
            self.plug_top_left_corner_x,
            self.y,
            self.size,
            self.size,
        )

        # # Paint the inner circle.
        # inner_size = self.size * .5
        # painter.setBrush(_qt.QBrush(self.inner_color))
        # painter.drawEllipse(
        #     x + (self.size - inner_size) * .5,
        #     self.y + (self.size - inner_size) * .5,
        #     inner_size,
        #     inner_size,
        # )

    def plug_center(self):
        """Return the center position of the plug part.

        :rtype: PySide.QtCore.QPointF
        """
        return _qtcore.QRectF(
            self.plug_top_left_corner_x,
            self.y,
            self.size,
            self.size,
        ).center()

    def mousePressEvent(self, event):
        """Initiate a `Connection` from this `Attribute`."""
        if event.button() != _qtcore.Qt.MouseButton.LeftButton:
            return
        if self.pending_connection:
            return

        if self.is_input:
            if self.connections:
                self.pending_connection = self.connections.values()[0]
                return

        self.pending_connection = _conn.Connection()
        self.pending_connection.setParentItem(self)
        self.pending_connection.source = self
        self.pending_connection.source_pos = self.plug_center()

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
        if not isinstance(destination, Attribute):
            self._delete_pending_connection()
        elif destination.name in self.connections:
            self._delete_pending_connection()
        else:
            self.pending_connection.destination = destination
            self.connections[destination.name] = self.pending_connection
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
