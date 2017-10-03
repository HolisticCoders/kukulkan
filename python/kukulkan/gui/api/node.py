import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.qt.QtCore as _qtcore


class Node(_qt.QGraphicsItem):
    """A node item that can be added to a graph."""

    def __init__(self, name, parent=None):
        super(Node, self).__init__(parent)
        self.name = name
        self.attributes = {}
        self.plugs = {}
        self.reset()

    def __str__(self):
        """Return the string form of the node (its name)."""
        return str(self.name)

    @property
    def connections(self):
        """Return the connections of this `Node`."""
        connections = {}
        for plug in [self.input, self.output]:
            if plug is None:
                continue
            connections.update(plug.connections)
        return connections

    def reset(self):
        """Reset the graphic state to its initial value."""
        self.setFlag(_qt.QGraphicsItem.ItemIsMovable)
        self.setFlag(_qt.QGraphicsItem.ItemIsSelectable)
        self.setFlag(_qt.QGraphicsItem.ItemIsFocusable)

        self.x = 0
        self.y = 0
        self.width = 200

        self.roundness = 5
        self.body_color = _qt.QColor(110, 110, 110)
        self.label_color = _qt.QColor(50, 50, 50)
        self.label_font = _qt.QFont(
            'Helvetica [Cronyx]',
            12,
            _qt.QFont.Bold
        )
        self.label_height = 30
        self.label_offset = 5

        self.attributes_spacing = 25

        self.height = self.label_height + self.attributes_spacing

    def add_attribute(self, name, attribute_type):
        if name in self.attributes:
            raise KeyError('{} already exists.'.format(self.attributes[name]))
        attribute = attribute_type(name, self)
        attribute.setParentItem(self)
        self.attributes[name] = attribute
        self.height += self.attributes_spacing + attribute.size
        attr_x = attribute.size * -0.5
        attr_y = (
            self.label_height
            + self.attributes_spacing * len(self.attributes)
            + attribute.size * (len(self.attributes) - 1)
        )
        attribute.setPos(attr_x, attr_y)
        return attribute

    def boundingRect(self):
        return _qtcore.QRectF(
            self.x,
            self.y,
            self.width,
            self.height,
        )

    def paint(self, painter, option, widget):
        self.paint_clip(painter, option, widget)
        self.paint_label(painter, option, widget)
        self.paint_body(painter, option, widget)
        self.paint_label_text(painter, option, widget)

    def paint_clip(self, painter, option, widget):
        # Clip the node to make it round.
        clip = _qt.QPainterPath()
        clip.addRoundedRect(
            self.x,
            self.y,
            self.width,
            self.height,
            self.roundness,
            self.roundness,
        )
        painter.setClipping(True)
        painter.setClipPath(clip)

        painter.setPen(_qtcore.Qt.NoPen)

    def paint_label(self, painter, option, widget):
        # Paint the label part.
        painter.setBrush(_qt.QBrush(self.label_color))
        painter.drawRect(
            self.x,
            self.y,
            self.width,
            self.label_height,
        )

    def paint_body(self, painter, option, widget):
        # Paint the body part.
        painter.setBrush(_qt.QBrush(self.body_color))
        painter.drawRect(
            self.x,
            self.y + self.label_height,
            self.width,
            self.height - self.label_height,
        )

    def paint_label_text(self, painter, option, widget):
        # Paint the label text
        painter.setFont(self.label_font)
        painter.setPen(self.body_color)
        painter.drawText(
            self.x + self.label_offset,
            self.y,
            self.width - self.label_offset,
            self.label_height,
            _qtcore.Qt.AlignVCenter | _qtcore.Qt.AlignLeft,
            self.name,
        )

    def mouseMoveEvent(self, event):
        super(Node, self).mouseMoveEvent(event)
        for attribute in self.attributes.values():
            for connection in attribute.connections.values():
                connection.compute_path()
