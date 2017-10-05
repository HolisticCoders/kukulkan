from kukulkan.config import UI

import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.qt.QtCore as _qtcore
import kukulkan.gui.api.attribute as _attribute


class Node(_qt.QGraphicsItem):
    """A node item that can be added to a graph."""

    def __init__(self, name, parent=None):
        super(Node, self).__init__(parent)
        self.name = name
        self.attributes = {}
        self.plugs = {}
        self.reset()

    def __str__(self):
        """Return the string form of the node (its name)."""
        return str(self.name)

    def __getattr__(self, name):
        try:
            attr = getattr(UI.node, name)
            return attr
        except AttributeError:
            err = 'Node object has no attribute {}.'.format(name)
            raise AttributeError(err)

    @property
    def connections(self):
        """Return the connections of this `Node`."""
        connections = {}
        for plug in [self.input, self.output]:
            if plug is None:
                continue
            connections.update(plug.connections)
        return connections

    def reset(self):
        """Reset the graphic state to its initial value."""
        self.setFlag(_qt.QGraphicsItem.ItemIsMovable)
        self.setFlag(_qt.QGraphicsItem.ItemIsSelectable)
        self.setFlag(_qt.QGraphicsItem.ItemIsFocusable)

        self.resizing = False

        self.x = 0
        self.y = 0

        self.highlighter = _qt.QPainterPathStroker()
        self.highlighter.setCapStyle(_qtcore.Qt.RoundCap)
        self.resize_handle_size = 10

    @property
    def base_height(self):
        return (
            UI.node.header.height
            + UI.attribute.spacing
            + self.resize_handle_size
        )

    @property
    def height(self):
        return (
            self.base_height
            + UI.attribute.spacing * len(self.attributes)
            + UI.attribute.size * (len(self.attributes) - 1)
        )

    def add_attribute(self, name, attribute_type, plug_type):
        if name in self.attributes:
            raise KeyError('{} already exists.'.format(self.attributes[name]))

        if plug_type == 'input':
            attribute = _attribute.Input
        elif plug_type == 'output':
            attribute = _attribute.Output
        else:
            return

        attribute = attribute(name, self, attribute_type)
        attribute.setParentItem(self)
        self.attributes[name] = attribute
        attr_x = attribute.size * -0.5
        attr_y = (
            UI.node.header.height
            + UI.attribute.spacing * len(self.attributes)
            + attribute.size * (len(self.attributes) - 1)
        )
        attribute.setPos(attr_x, attr_y)
        return attribute

    def boundingRect(self):
        return _qtcore.QRectF(
            self.x - UI.node.highlight.padding,
            self.y - UI.node.highlight.padding,
            UI.node.width + UI.node.highlight.padding * 2,
            self.height + UI.node.highlight.padding * 2,
        )

    def paint(self, painter, option, widget):
        if self.isSelected():
            self.paint_highlight(painter, option, widget)
        self.paint_clip(painter, option, widget)
        self.paint_body(painter, option, widget)
        self.paint_label(painter, option, widget)
        # self.paint_resize_handle(painter, option, widget)
        self.paint_label_text(painter, option, widget)

    def paint_highlight(self, painter, option, widget):
        """Highlight the node.

        Called when the node is selected.
        """
        path = _qt.QPainterPath()
        path.addRoundedRect(
            self.x,
            self.y,
            UI.node.width,
            self.height,
            UI.node.roundness,
            UI.node.roundness,
        )
        self.highlighter.setWidth(UI.node.highlight.padding * 2)
        outline = self.highlighter.createStroke(path)
        color = _qt.QColor(*UI.node.highlight.brush)
        painter.fillPath(outline, _qt.QBrush(color))

    def paint_clip(self, painter, option, widget):
        # Clip the node to make it round.
        clip = _qt.QPainterPath()
        clip.addRoundedRect(
            self.x,
            self.y,
            UI.node.width,
            self.height,
            UI.node.roundness,
            UI.node.roundness,
        )
        painter.setClipping(True)
        painter.setClipPath(clip)

        painter.setPen(_qtcore.Qt.NoPen)

    def paint_label(self, painter, option, widget):
        # Paint the label part.
        painter.setBrush(_qt.QBrush(_qt.QColor(*UI.node.header.brush)))
        painter.drawRect(
            self.x,
            self.y,
            UI.node.width,
            UI.node.header.height,
        )

    def paint_body(self, painter, option, widget):
        # Paint the body part.
        painter.setBrush(_qt.QBrush(_qt.QColor(*UI.node.body.brush)))
        painter.drawRect(
            self.x,
            self.y + UI.node.header.height,
            UI.node.width,
            self.height - UI.node.header.height,
        )

    def paint_label_text(self, painter, option, widget):
        # Paint the label text
        font = _qt.QFont(
            UI.node.label.font.family,
            UI.node.label.font.size,
            UI.node.label.font.weight,
        )
        painter.setFont(font)
        painter.setPen(_qt.QColor(*UI.node.label.pen))
        painter.drawText(
            self.x + UI.node.label.offset,
            self.y,
            UI.node.width - UI.node.label.offset,
            UI.node.header.height,
            _qtcore.Qt.AlignVCenter | _qtcore.Qt.AlignLeft,
            self.name,
        )

    def paint_resize_handle(self, painter, option, widget):
        """Paint the footer region of the node.
        """
        painter.setBrush(_qt.QBrush(_qt.QColor(*UI['header']['brush'])))
        painter.drawRect(
            self.x,
            self.y + self.height - self.resize_handle_size,
            UI.node.width,
            self.resize_handle_size,
        )

    # def resize_handle_clicked(self, event):
    #     """Return `True` if the resize handle was clicked.
    #
    #     :rtype: bool
    #     """
    #     height_start = self.y + self.height - self.resize_handle_size
    #     height_end = self.y + self.height
    #     cond_height = height_start <= event.pos().y() <= height_end
    #     if not cond_height:
    #         return False
    #     width_start = self.x + UI.node.width - self.resize_handle_size
    #     width_end = self.x + UI.node.width
    #     cond_width = width_start <= event.pos().x() <= width_end
    #     if not cond_width:
    #         return False
    #     return True
    #
    # def resize_event(self, event):
    #     """Resize this node by the resize handle."""
    #     offset = event.pos() - self.resize_pos
    #     UI.node.width += offset.x()
    #     self.resize_pos = event.pos()
    #
    # def mousePressEvent(self, event):
    #     super(Node, self).mousePressEvent(event)
    #     if self.resize_handle_clicked(event):
    #         self.resize_pos = event.pos()
    #         self.resizing = True
    #
    # def mouseMoveEvent(self, event):
    #     if self.resizing:
    #         self.resize_event(event)
    #     else:
    #         super(Node, self).mouseMoveEvent(event)
    #
    # def mouseReleaseEvent(self, event):
    #     super(Node, self).mouseReleaseEvent(event)
    #     self.resizing = False

    # def mouseMoveEvent(self, event):
    #     super(Node, self).mouseMoveEvent(event)
    #     for attribute in self.attributes.values():
    #         for connection in attribute.connections.values():
    #             connection.compute_path()
