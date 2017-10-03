import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.qt.QtCore as _qtcore
import kukulkan.gui.api.plug as _plug


class Attribute(_qt.QGraphicsItem):

    def __init__(self, name, node, attribute_type):
        super(Attribute, self).__init__(node)
        self.name = name
        self.node = node
        self.value = None
        self.plug = None

        self.reset()
        self._create_plug()
        self.base_widget = attribute_type(self.name, self.node, self)
        self.base_widget = self.scene().addWidget(self.base_widget)
        self.base_widget.setParentItem(self)
        widget_height = self.base_widget.widget().height()
        widget_offset = (self.size - widget_height) / 2
        self.base_widget.setPos(
            self.widget_x,
            self.y + widget_offset
        )

    def __str__(self):
        """Return the attribute string form."""
        return '.'.join(map(str, [self.node, self.name]))

    @property
    def connections(self):
        """Return the connections of this `Attribute`."""
        connections = {}
        if self.plug is not None:
            connections.update(self.plug.connections)
            return connections

    def reset(self):
        """Reset the graphic state to its initial value."""
        self.x = 0
        self.y = 0
        self.size = 15
        self.width = self.node.width + self.size
        self.widget_x = self.x + self.size 


    def boundingRect(self):
        return _qtcore.QRectF(
            self.x,
            self.y,
            self.width,
            self.size,
        )

    def paint(self, painter, option, widget):
        pass

    def _create_plug(self):
        """Create the default plug for this `Attribute`.

        Override this in the subclasses
        """

class Input(Attribute):

    def __init__(self, *args, **kwargs):
        super(Input, self).__init__(*args, **kwargs)

    def _create_plug(self):
        """Create an input plug."""
        self.plug = _plug.Input(self)


class Output(Attribute):

    def __init__(self, *args, **kwargs):
        super(Output, self).__init__(*args, **kwargs)

    def _create_plug(self):
        """Create an input plug."""
        self.plug = _plug.Output(self)
        self.plug.setPos(
            self.width - self.size,
            self.y
        )