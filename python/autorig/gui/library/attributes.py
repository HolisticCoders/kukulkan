from autorig.gui.api.attribute import Attribute
import autorig.gui.qt.QtGui as _qt
import autorig.gui.qt.QtCore as _qtcore


class MessageAttribute(Attribute):
    """Simple attribute that is used to connect nodes."""


class NumericAttribute(Attribute):
    """Base class for numeric attributes."""
    def paint_label(self, painter, option, widget):
        self.spinbox.setPos(self.x + self.size + 5, self.y)
        super(NumericAttribute, self).paint_label(painter, option, widget)


class FloatAttribute(NumericAttribute):
    """Float attribute."""
    def __init__(self, *args, **kwargs):
        super(NumericAttribute, self).__init__(*args, **kwargs)
        self.spinbox = self.scene().addWidget(_qt.QDoubleSpinBox())
        self.spinbox.setParentItem(self)
        self.label_offset = self.size + 5


class IntAttribute(NumericAttribute):
    """Int attribute."""
    def __init__(self, *args, **kwargs):
        super(NumericAttribute, self).__init__(*args, **kwargs)
        self.spinbox = self.scene().addWidget(_qt.QSpinBox())
        self.spinbox.setParentItem(self)
        self.label_offset = self.size + 5


class BoolAttribute(Attribute):
    """Bool attribute."""


class StringAttribute(Attribute):
    """String attribute."""


class EnumAttribute(Attribute):
    """Enum attribute."""


class ColorAttribute(Attribute):
    """Color attribute."""
