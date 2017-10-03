import kukulkan.gui.api.attribute as _attribute
import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.qt.QtCore as _qtcore

class AttributeType(_qt.QWidget):
    def __init__(self, name, node, parent_item, *args, **kwargs):
        super(AttributeType, self).__init__(*args, **kwargs)
        self.name = name
        self.node = node
        self.parent_item = parent_item
        self.reset()
        self.create_widget()
        if self.widget:
            self.left_layout.addWidget(self.widget)
        if isinstance(self.parent_item, _attribute.Input):
            self.left_layout.addWidget(self.widget)
            self.right_layout.addWidget(self.label)
        else:
            self.left_layout.addWidget(self.label)
            self.right_layout.addWidget(self.widget)

    def reset(self):
        self.myWidth = self.node.width - self.parent_item.size
        self.myHeight = 50
        self.setStyleSheet("background-color: transparent")
        self.resize(self.myWidth , self.myHeight)
        self.layout = _qt.QHBoxLayout()
        self.setLayout(self.layout)

        self.left_layout = _qt.QHBoxLayout()
        self.right_layout = _qt.QHBoxLayout()
        self.left_layout.setAlignment(_qtcore.Qt.AlignLeft)
        self.right_layout.setAlignment(_qtcore.Qt.AlignRight)
        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.right_layout)

        self.label = _qt.QLabel(self.name)
        self.right_layout.addWidget(self.label)

    def create_widget(self):
        """Create the widget of this attribute.

        Override when subclassing to add a widget to the attribute.
        You want to set the variable self.widget like so:
            self.widget = self.scene().addWidget(_qt.QDoubleSpinBox())
        This is also the place to set the label_offset and anything that
        is affected by the presence of the widget.
        """


class Message(AttributeType):
    """Simple attribute that is used to connect nodes."""


class Numeric(AttributeType):
    """Base class for numeric attributes."""


class Float(Numeric):
    """Float attribute."""
    def create_widget(self):
        super(Float, self).create_widget()
        self.widget = _qt.QDoubleSpinBox()


class Integer(Numeric):
    """Int attribute."""
    def create_widget(self):
        super(Integer, self).create_widget()
        self.widget = _qt.QSpinBox()


class Boolean(AttributeType):
    """Bool attribute."""
    def create_widget(self):
        super(Boolean, self).create_widget()
        self.widget = _qt.QCheckBox()


class String(AttributeType):
    """String attribute."""
    def create_widget(self):
        super(String, self).create_widget()
        self.widget = _qt.QLineEdit()


class Enum(AttributeType):
    """Enum attribute."""
    def create_widget(self):
        super(Enum, self).create_widget()
        self.widget = _qt.QComboBox()


class Color(AttributeType):
    """Color attribute."""
