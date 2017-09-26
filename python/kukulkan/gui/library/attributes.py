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
        self.label_offset = self.size + 5


class IntAttribute(NumericAttribute):
    """Int attribute."""
    def create_widget(self):
        super(IntAttribute, self).create_widget()
        self.widget = self.scene().addWidget(_qt.QSpinBox())
        self.label_offset = self.size + 5


class BoolAttribute(Attribute):
    """Bool attribute."""
    def create_widget(self):
        super(BoolAttribute, self).create_widget()
        self.widget = self.scene().addWidget(_qt.QCheckBox())
        self.label_offset = self.size + 5


class StringAttribute(Attribute):
    """String attribute."""
    def create_widget(self):
        super(StringAttribute, self).create_widget()
        self.widget = self.scene().addWidget(_qt.QLineEdit())
        self.label_offset = self.size + 5


class EnumAttribute(Attribute):
    """Enum attribute."""
    def create_widget(self):
        super(EnumAttribute, self).create_widget()
        self.widget = self.scene().addWidget(_qt.QComboBox())
        self.label_offset = self.size + 5


class ColorAttribute(Attribute):
    """Color attribute."""
