import autorig.gui.qt.QtGui as _qt
import autorig.gui.qt.QtCore as _qtcore


class Attribute(_qt.QGraphicsEllipseItem):

    default_geo = _qtcore.QRectF(0, 30, 15, 15)

    def __init__(self, name, parent=None):
        super(Attribute, self).__init__(parent)
        self.setRect(self.default_geo)
        self.name = name

    def paint(self, painter, option, widget):
        painter.drawEllipse(self.default_geo)
        painter.drawText(20, 0, self.name)
