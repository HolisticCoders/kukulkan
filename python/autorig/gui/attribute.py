import autorig.gui.qt.QtGui as _qt
import autorig.gui.qt.QtCore as _qtcore


class Attribute(_qt.QGraphicsItem):

    def __init__(self, name, node):
        super(Attribute, self).__init__(node)
        self.name = name
        self.node = node
        self.connections = {}
        self.reset()

    def reset(self):
        self.x = 0
        self.y = 0
        self.size = 20
        self.width = self.node.width + self.size

        self.label_font = _qt.QFont(
            'Helvetica [Cronyx]',
            10,
        )

        self.inner_color = _qt.QColor(53, 53, 53)
        self.outer_color = _qt.QColor(200, 180, 150)
        # self.border_color = _qt.QColor(20, 20, 20)
        # self.border_width = 10

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

        # Paint the outer circle.
        painter.setBrush(_qt.QBrush(self.outer_color))
        painter.drawEllipse(
            self.x,
            self.y,
            self.size,
            self.size,
        )

        # Paint the inner circle.
        inner_size = self.size * .5
        painter.setBrush(_qt.QBrush(self.inner_color))
        painter.drawEllipse(
            self.x + (self.size - inner_size) * .5,
            self.y + (self.size - inner_size) * .5,
            inner_size,
            inner_size,
        )

        painter.setFont(self.label_font)
        painter.setPen(self.node.label_color)
        painter.drawText(
            self.x,
            self.y,
            self.width,
            self.size,
            _qtcore.Qt.AlignCenter,
            self.name,
        )

    # def connect(self, destination):
    #     """Connect this `Attribute` to another one.
    #
    #     This `Attribute` will be the source, and the ``destination`` will be
    #     the driven `Attribute`.
    #
    #     :param destination: Destination attribute.
    #     :type destination: Attribute.
    #     """

    def mousePressEvent(self):
        """Create a `Connection` object from this attribute."""
