from functools import partial

import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.qt.QtCore as _qtcore
import kukulkan.gui.qt.styled_widgets as _styled_widgets


class AttributeWidget(_qt.QWidget):
    def __init__(self, name, node, attribute, *args, **kwargs):
        super(AttributeWidget, self).__init__(*args, **kwargs)
        self.name = name
        self.node = node
        self._value = None
        self.attribute = attribute
        self.widget = None
        self.reset()
        self.create_widget()
        if self.widget:
            self.update_value_from_widget()
            self.left_layout.addWidget(self.widget)
        if self.attribute.is_input:
            self.left_layout.addWidget(self.widget)
            self.right_layout.addWidget(self.label)
        elif self.attribute.is_output:
            self.left_layout.addWidget(self.label)
            self.right_layout.addWidget(self.widget)

    def reset(self):
        self.myWidth = self.node.width - self.attribute.size
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

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.update_widget_value(value)
        if self.attribute.value != value:
            self.attribute.value = value

    def create_widget(self):
        """Create the widget of this widget.

        Override when subclassing to add a widget to the attribute.
        You want to set the variable self.widget like so:
            self.widget = _qt.QSpinBox()
        """

    def update_value_from_widget(self):
        """Update the value of this container widget.

        This method should be called by a signal of the contained widget.
        It should also be override in the subclasses.
        """

    def update_widget_value(self, value):
        """Update the value of this contained widget.

        override this method in the subclasses
        """


class Message(AttributeWidget):
    """Simple attribute that is used to connect nodes."""


class Numeric(AttributeWidget):
    """Base class for numeric attributes."""
    def update_value_from_widget(self):
        super(Numeric, self).update_value_from_widget()
        self.value = self.widget.value()

    def update_widget_value(self, value):
        super(Numeric, self).update_widget_value(value)
        self.widget.setValue(value)


class Integer(Numeric):
    """Int attribute."""
    def create_widget(self):
        """Create a QSpinBox."""
        super(Integer, self).create_widget()
        self.widget = _styled_widgets.SpinBox()
        self.widget.valueChanged.connect(self.update_value_from_widget)


class Float(Numeric):
    """Float attribute."""
    def create_widget(self):
        """Create a QDoubleSpinBox."""
        super(Float, self).create_widget()
        self.widget = _styled_widgets.DoubleSpinBox()
        self.widget.valueChanged.connect(self.update_value_from_widget)


class Boolean(AttributeWidget):
    """Bool attribute."""
    def create_widget(self):
        """Create a QCheckBox."""
        super(Boolean, self).create_widget()
        self.widget = _qt.QCheckBox()
        self.widget.setTristate(False)
        self.widget.stateChanged.connect(self.update_value_from_widget)

    def update_value_from_widget(self):
        super(Boolean, self).update_value_from_widget()
        self.value = self.widget.isChecked()

    def update_widget_value(self, value):
        super(Boolean, self).update_widget_value(value)
        self.widget.setChecked(value)


class String(AttributeWidget):
    """String attribute."""
    def create_widget(self):
        """Create a QLineEdit."""
        super(String, self).create_widget()
        self.widget = _styled_widgets.LineEdit()
        self.widget.editingFinished.connect(self.update_value_from_widget)

    def update_value_from_widget(self):
        super(String, self).update_value_from_widget()
        self.value = self.widget.text()

    def update_widget_value(self, value):
        super(String, self).update_widget_value(value)
        self.widget.setText(value)


class Enum(AttributeWidget):
    """Enum attribute."""
    def create_widget(self):
        """Create a QComboBox."""
        super(Enum, self).create_widget()
        self.widget = _styled_widgets.ComboBox()
        self.widget.currentIndexChanged.connect(self.update_value_from_widget)

    def update_value_from_widget(self):
        super(Enum, self).update_value_from_widget()
        self.value = self.widget.currentIndex()

    def update_widget_value(self, value):
        super(Enum, self).update_widget_value(value)
        self.widget.setCurrentIndex(value)

map_widgets = {
    'message': Message,
    'integer': Integer,
    'float': Float,
    'boolean': Boolean,
    'string': String,
    'enum': Enum,
}