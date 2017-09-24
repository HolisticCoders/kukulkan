import autorig.gui.qt.QtGui as _qt
import autorig.gui.qt.QtCore as _qtcore
import autorig.gui.api.plug as _plug


class Attribute(_qt.QGraphicsItem):

    is_input = True
    is_output = True

    def __init__(self, name, node):
        super(Attribute, self).__init__(node)
        self.name = name
        self.node = node
        self._value = None
        self.input = None
        self.output = None
        self.connections = {}
        self.reset()
        self._create_plugs()

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
        """Reset the graphic state to its initial value."""
        self.x = 0
        self.y = 0
        self.size = 15
        self.width = self.node.width + self.size
        self.label_font = _qt.QFont(
            'Helvetica [Cronyx]',
            10,
        )
        self.label_offset = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def boundingRect(self):
        return _qtcore.QRectF(
            self.x,
            self.y,
            self.width,
            self.size,
        )

    def paint(self, painter, option, widget):
        painter.setPen(_qtcore.Qt.NoPen)
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

    def _create_plugs(self):
        """Create the default plugs for this `Attribute`.

        Default input is created if `Attribute.is_input` is `True`, and
        default output is if `Attribute.is_output` is `True`.
        """
        if self.is_input:
            self._add_input()
        if self.is_output:
            self._add_output()

    def _add_input(self):
        """Add an input plug to this attribute."""
        self.input = _plug.Input(self)

    def _add_output(self):
        """Add an output plug to this attribute."""
        self.output = _plug.Output(self)
        self.output.setPos(
            self.width - self.size,
            self.y
        )
