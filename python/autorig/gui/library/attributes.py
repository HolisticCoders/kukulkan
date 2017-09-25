from autorig.gui.api.attribute import Attribute
import autorig.gui.qt.QtGui as _qt
import autorig.gui.qt.QtCore as _qtcore


class MessageAttribute(Attribute):
    """Simple attribute that is used to connect nodes."""


class NumericAttribute(Attribute):
    """Base class for numeric attributes."""


class FloatAttribute(NumericAttribute):
    """Float attribute."""
    def __init__(self, *args, **kwargs):
        super(FloatAttribute, self).__init__(*args, **kwargs)
        self.widget = self.scene().addWidget(_qt.QDoubleSpinBox())
        self.widget.setParentItem(self)
        self.widget.setPos(self.x + self.size + 5, self.y)
        self.label_offset = self.size + 5


class IntAttribute(NumericAttribute):
    """Int attribute."""
    def __init__(self, *args, **kwargs):
        super(IntAttribute, self).__init__(*args, **kwargs)
        self.widget = self.scene().addWidget(_qt.QSpinBox())
        self.widget.setParentItem(self)
        self.widget.setPos(self.x + self.size + 5, self.y)
        self.label_offset = self.size + 5


class BoolAttribute(Attribute):
    """Bool attribute."""
    def __init__(self, *args, **kwargs):
        super(BoolAttribute, self).__init__(*args, **kwargs)
        self.widget = self.scene().addWidget(_qt.QCheckBox())
        self.widget.setParentItem(self)
        self.widget.setPos(self.x + self.size + 5, self.y)
        self.label_offset = self.size + 5


class StringAttribute(Attribute):
    """String attribute."""
    def __init__(self, *args, **kwargs):
        super(StringAttribute, self).__init__(*args, **kwargs)
        self.widget = self.scene().addWidget(_qt.QLineEdit())
        self.widget.setParentItem(self)
        self.widget.setPos(self.x + self.size + 5, self.y)
        self.label_offset = self.size + 5


class EnumAttribute(Attribute):
    """Enum attribute."""
    def __init__(self, *args, **kwargs):
        super(EnumAttribute, self).__init__(*args, **kwargs)
        self.widget = self.scene().addWidget(_qt.QComboBox())
        self.widget.setParentItem(self)
        self.widget.setPos(self.x + self.size + 5, self.y)
        self.label_offset = self.size + 5


class ColorAttribute(Attribute):
    """Color attribute."""
