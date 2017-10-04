from functools import partial

import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.qt.QtCore as _qtcore


class AttributeWidget(_qt.QWidget):
    def __init__(self, name, node, parent_item, *args, **kwargs):
        super(AttributeWidget, self).__init__(*args, **kwargs)
        self.name = name
        self.node = node
        self.value = None
        self.parent_item = parent_item
        self.widget = None
        self.reset()
        self.create_widget()
        if self.widget:
            self.left_layout.addWidget(self.widget)
        if self.parent_item.is_input:
            self.left_layout.addWidget(self.widget)
            self.right_layout.addWidget(self.label)
        elif self.parent_item.is_output:
            self.left_layout.addWidget(self.label)
            self.right_layout.addWidget(self.widget)

    def reset(self):
        self.myWidth = self.node.width - self.parent_item.size
        self.myHeight = 50
        self.setStyleSheet("background-color: transparent")
        self.resize(self.myWidth, self.myHeight)
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
        """Create the widget of this widget.

        Override when subclassing to add a widget to the attribute.
        You want to set the variable self.widget like so:
            self.widget = _qt.QSpinBox()
        """

    def update_value(self, value):
        """Update the value of this container widget.

        This method should be called by a signal of the contained widget.
        """
        self.value = value


class Message(AttributeWidget):
    """Simple attribute that is used to connect nodes."""


class Numeric(AttributeWidget):
    """Base class for numeric attributes."""


class Integer(Numeric):
    """Int attribute."""
    def create_widget(self):
        """Create a QSpinBox."""
        super(Integer, self).create_widget()
        self.widget = _qt.QSpinBox()
        self.widget.valueChanged.connect(self.update_value)


class Float(Numeric):
    """Float attribute."""
    def create_widget(self):
        """Create a QDoubleSpinBox."""
        super(Float, self).create_widget()
        self.widget = _qt.QDoubleSpinBox()
        self.widget.valueChanged.connect(self.update_value)


class Boolean(AttributeWidget):
    """Bool attribute."""
    def create_widget(self):
        """Create a QCheckBox."""
        super(Boolean, self).create_widget()
        self.widget = _qt.QCheckBox()
        self.widget.stateChanged.connect(self.update_value)


class String(AttributeWidget):
    """String attribute."""
    def create_widget(self):
        """Create a QLineEdit."""
        super(String, self).create_widget()
        self.widget = _qt.QLineEdit()
        self.widget.editingFinished.connect(self.update_value)

    def update_value(self):
        self.value = self.widget.text()


class Enum(AttributeWidget):
    """Enum attribute."""
    def create_widget(self):
        """Create a QComboBox."""
        super(Enum, self).create_widget()
        self.widget = _qt.QComboBox()

        self.widget.currentIndexChanged.connect(self.update_value)

map_widgets = {
    'message': Message,
    'integer': Integer,
    'float': Float,
    'boolean': Boolean,
    'string': String,
    'enum': Enum,
}