import math

import kukulkan.events
from kukulkan.config import UI

import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.qt.QtCore as _qtcore
import kukulkan.gui.api.node as _node


class Graph(_qt.QGraphicsScene):
    """A graph scene."""

    def add_node(self, name):
        node = _node.Node(name)
        self.addItem(node)
        return node


class GraphView(_qt.QGraphicsView):
    """A graphical view."""

    def __init__(self, *args, **kwargs):
        super(GraphView, self).__init__(*args, **kwargs)
        self.panning = False
        self.panning_speed = 1
        self.zooming = False
        self.zooming_speed = .1
        self.zooming_speed_wheel = .1
        self.scale_factor = 1
        self.setSceneRect(-2500, -2500, 5000, 5000)
        self.setHorizontalScrollBarPolicy(_qtcore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(_qtcore.Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(_qt.QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(_qt.QGraphicsView.FullViewportUpdate)
        kukulkan.events.subscribe(self.refresh, 'config.ui.changed')

    def pan_event(self, event):
        """Pan the view.

        Move from `GraphView.panning_pos` to ``event``.
        """
        offset = (event.pos() - self.panning_pos) * self.panning_speed
        start = self.viewport().rect().center()
        center = self.mapToScene(start - offset).toPoint()
        self.centerOn(center)
        self.panning_pos = event.pos()

    def zoom_event(self, event):
        """Zoom in or out the view."""
        offset = (event.pos() - self.zooming_pos) * self.zooming_speed
        direction = offset.x() - offset.y()
        scale = 1
        if direction > 0:
            scale += offset.manhattanLength() * self.zooming_speed
        elif direction < 0:
            scale -= offset.manhattanLength() * self.zooming_speed
        self.scale(scale, scale)
        self.zooming_pos = event.pos()

    def mousePressEvent(self, event):
        if event.button() == _qtcore.Qt.LeftButton:
            self.setDragMode(_qt.QGraphicsView.RubberBandDrag)
        elif event.button() == _qtcore.Qt.MiddleButton:
            self.panning = True
            self.panning_pos = event.pos()
        super(GraphView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.panning:
            self.pan_event(event)
            return
        super(GraphView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super(GraphView, self).mouseReleaseEvent(event)
        self.setDragMode(_qt.QGraphicsView.NoDrag)
        self.panning = False
        self.zooming = False

    def wheelEvent(self, event):
        scale = 1
        if event.delta() > 0:
            scale += self.zooming_speed_wheel
        elif event.delta() < 0:
            scale -= self.zooming_speed_wheel
        self.scale(scale, scale)
        self.scale_factor *= scale

    def drawBackground(self, painter, rect):
        painter.setBrush(_qt.QColor(*UI.graph.brush))
        painter.setPen(_qt.QColor(*UI.graph.grid.pen))
        step = UI.graph.grid.step
        top = rect.top() - (rect.top() % step)
        bottom = rect.bottom()  # - (rect.bottom() % step)
        left = rect.left() - (rect.left() % step)
        right = rect.right()  # - (rect.right() % step)

        lines = []

        x = left
        while x <= right:
            line = _qtcore.QLine(x, top, x, bottom)
            lines.append(line)
            x += step

        y = top
        while y <= bottom:
            line = _qtcore.QLine(left, y, right, y)
            lines.append(line)
            y += step

        # If the scene is very large, do not draw all the lines.
        size_factor = 1 / max(self.scale_factor, .0000001)
        skip_n = int(math.ceil((size_factor - 1) / 3.))
        if size_factor > 2:
            lines = lines[::skip_n]

        painter.drawRect(rect)
        painter.drawLines(lines)

    def refresh(self):
        """Force the update of this view."""
        self.scene().update(
            self.viewport().rect().adjusted(-100, -100, 200, 200)
        )
