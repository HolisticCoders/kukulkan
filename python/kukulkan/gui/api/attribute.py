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
        if self.widget:
            self.left_layout.addWidget(self.widget)
            # really temp stuff
            # self.widget.setStyleSheet("background-color: #232729")


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
        self.label_offset = 5
        # TODO: This needs to change based on is_input/is_output
        self.label_x = self.x + self.label_offset
        self.label_width = self.width
        self.label_alignment = _qtcore.Qt.AlignRight
        self.widget_x = self.x + self.size 

    def create_widget(self):
        """Create the widget of this attribute.

        Override when subclassing to add a widget to the attribute.
        You want to set the variable self.widget like so:
            self.widget = self.scene().addWidget(_qt.QDoubleSpinBox())
        This is also the place to set the label_offset and anything that
        is affected by the presence of the widget.
        """
        baseWidget = _qt.QWidget()
        baseWidget.setStyleSheet("background-color: transparent")
        baseWidget.resize(self.node.width - self.size, 50)
        layout = _qt.QHBoxLayout()
        baseWidget.setLayout(layout)

        self.left_layout = _qt.QHBoxLayout()
        self.right_layout = _qt.QHBoxLayout()
        self.left_layout.setAlignment(_qtcore.Qt.AlignLeft)
        self.right_layout.setAlignment(_qtcore.Qt.AlignRight)
        layout.addLayout(self.left_layout)
        layout.addLayout(self.right_layout)

        self.label = _qt.QLabel(self.name)
        self.right_layout.addWidget(self.label)
        self.baseWidget = self.scene().addWidget(baseWidget)
        self.baseWidget.setParentItem(self)
        widget_height = self.baseWidget.widget().height()
        widget_offset = (self.size - widget_height) / 2
        self.baseWidget.setPos(
            self.widget_x,
            self.y + widget_offset
        )


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
        old_value = self.is_input
        if value != old_value:
            self._is_input = value
            if value is False:
                self._del_input()
                if self.is_output:
                    self.right_layout.removeWidget(self.label)
                    self.left_layout.removeWidget(self.widget)
                    self.right_layout.addWidget(self.widget)
                    self.left_layout.addWidget(self.label)

    @property
    def is_output(self):
        return self._is_output

    @is_output.setter
    def is_output(self, value):
        old_value = self.is_output
        if value != old_value:
            self._is_output = value
            if value is False:
                self._del_output()
                if self.is_input:
                    self.left_layout.removeWidget(self.label)
                    self.right_layout.removeWidget(self.widget)
                    self.left_layout.addWidget(self.widget)
                    self.right_layout.addWidget(self.label)

    def boundingRect(self):
        return _qtcore.QRectF(
            self.x,
            self.y,
            self.width,
            self.size,
        )

    def paint(self, painter, option, widget):
        painter.setPen(_qtcore.Qt.NoPen)
        # self.paint_label(painter, option, widget)

    def paint_label(self, painter, option, widget):
        """Paint the label of the attribute, on the node."""
        painter.setFont(self.label_font)
        painter.setPen(self.node.label_color)
        painter.drawText(
            self.label_x,
            self.y,
            self.label_width,
            self.size,
            self.label_alignment,
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
