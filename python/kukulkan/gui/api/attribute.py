import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.qt.QtCore as _qtcore
import kukulkan.gui.api.plug as _plug


class Attribute(_qt.QGraphicsItem):

    def __init__(self, name, node, is_input=True, is_output=True):
        super(Attribute, self).__init__(node)
        self.name = name
        self.node = node
        self._value = None
        self.widget = None
        self.input = None
        self.output = None
        self._is_input = is_input
        self._is_output = is_output
        self.reset()
        self._create_plugs()
        self.create_widget()
        if self.widget is not None:
            self._place_widget()

    def __str__(self):
        """Return the attribute string form."""
        return '.'.join(map(str, [self.node, self.name]))

    @property
    def connections(self):
        """Return the connections of this `Attribute`."""
        connections = {}
        for plug in [self.input, self.output]:
            if plug is None:
                continue
            connections.update(plug.connections)
        return connections

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

    def create_widget(self):
        """Create the widget of this attribute.

        Override when subclassing to add a widget to the attribute.
        You want to set the variable self.widget like so:
            self.widget = self.scene().addWidget(_qt.QDoubleSpinBox())
        This is also the place to set the label_offset and anything that
        is affected by the presence of the widget.
        """

    def _place_widget(self):
        self.widget.setParentItem(self)
        widget_height = self.widget.widget().height()
        widget_offset = (self.size - widget_height) / 2
        self.widget.setPos(
            self.x + self.size + 5,
            self.y + widget_offset
        )
        self.label_offset = self.widget.widget().width() - 40

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def is_input(self):
        return self._is_input

    @is_input.setter
    def is_input(self, value):
        self._is_input = value
        if value == False:
            self._del_input()

    @property
    def is_output(self):
        return self._is_output

    @is_output.setter
    def is_output(self, value):
        self._is_output = value
        if value == False:
            self._del_output()

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

    def _del_input(self):
        if self.input not in self.scene().items():
            return
        self.scene().removeItem(self.input)
        self._is_input = False

    def _del_output(self):
        if self.output not in self.scene().items():
            return
        self.scene().removeItem(self.output)
        self._is_output = False
