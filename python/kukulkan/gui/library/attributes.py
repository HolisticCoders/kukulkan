from kukulkan.gui.api.attribute import Attribute
import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.qt.QtCore as _qtcore


class MessageAttribute(Attribute):
    """Simple attribute that is used to connect nodes."""


class NumericAttribute(Attribute):
    """Base class for numeric attributes."""


class FloatAttribute(NumericAttribute):
    """Float attribute."""
    def create_widget(self):
        super(FloatAttribute, self).create_widget()
        self.widget = self.scene().addWidget(_qt.QDoubleSpinBox())


class IntAttribute(NumericAttribute):
    """Int attribute."""
    def create_widget(self):
        super(IntAttribute, self).create_widget()
        self.widget = self.scene().addWidget(_qt.QSpinBox())


class BoolAttribute(Attribute):
    """Bool attribute."""
    def create_widget(self):
        super(BoolAttribute, self).create_widget()
        self.widget = self.scene().addWidget(_qt.QCheckBox())


class StringAttribute(Attribute):
    """String attribute."""
    def create_widget(self):
        super(StringAttribute, self).create_widget()
        self.widget = self.scene().addWidget(_qt.QLineEdit())
        self.widget.widget().resize(75, 31)


class EnumAttribute(Attribute):
    """Enum attribute."""
    def create_widget(self):
        super(EnumAttribute, self).create_widget()
        self.widget = self.scene().addWidget(_qt.QComboBox())


class ColorAttribute(Attribute):
    """Color attribute."""
