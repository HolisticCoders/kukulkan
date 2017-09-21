import autorig.gui.qt.QtGui as _qt
import autorig.gui.qt.QtCore as _qtcore
import autorig.gui.jong.attribute as _attr


class Node(_qt.QGraphicsRectItem):
    """A node item that can be added to a graph."""

    default_geo = _qtcore.QRectF(0, 0, 100, 160)

    def __init__(self, name, parent=None):
        super(Node, self).__init__(parent)
        self.name = name
        self.attributes = {}
        self.reset()

    def reset(self):
        self.setFlag(_qt.QGraphicsItem.ItemIsMovable)
        self.setFlag(_qt.QGraphicsItem.ItemIsSelectable)
        self.setFlag(_qt.QGraphicsItem.ItemIsFocusable)
        self.setRect(self.default_geo)

        self.x = self.default_geo.x()
        self.y = self.default_geo.y()
        self.width = self.default_geo.width()
        self.height = self.default_geo.height()
        self.roundness = 5
        self.body_color = _qt.QColor(100, 100, 100)
        self.label_color = _qt.QColor(50, 50, 50)
        self.label_font = _qt.QFont('Helvetica [Cronyx]', 12, _qt.QFont.Bold)
        self.label_height = 20
        self.label_offset = 15

    def add_attribute(self, name):
        attribute = _attr.Attribute(name)
        self.attributes[name] = attribute
        self.addToGroup(attribute)
        return attribute

    def paint(self, painter, option, widget):
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

        # Paint the label part.
        painter.setBrush(_qt.QBrush(self.label_color))
        painter.drawRect(
            self.x,
            self.y,
            self.width,
            self.label_height,
        )

        # Paint the body part.
        painter.setBrush(_qt.QBrush(self.body_color))
        painter.drawRect(
            self.x,
            self.y + self.label_height,
            self.width,
            self.height - self.label_height,
        )

        # Paint the label
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
