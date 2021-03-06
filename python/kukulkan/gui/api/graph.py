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
        painter.drawRect(rect)

        for i, lines in enumerate(self.get_grid_lines(rect)):
            color = _qt.QColor(*UI.graph.grid.lines[i]['pen'])
            thickness = UI.graph.grid.lines[i]['thickness']
            painter.setPen(_qt.QPen(color, thickness))
            painter.drawLines(lines)

    def get_grid_lines(self, rect):
        """Return grid lines to draw.

        Returned value contains multiple lists, as there will
        be lines of different weight.
        Thiner lines are returned first.

        :param rect: Area to cover with lines.
        :type rect: PySide.QtCore.QRectF
        :rtype: list(list(PySide.QtCore.QLine))
        """
        h_lines, v_lines = self._get_base_lines(rect)

        # If the scene is very large, do not draw all the lines.
        size_factor = 1 / max(self.scale_factor, .0000001)
        skip_n = int(math.ceil((size_factor - 1) / 3.))
        if size_factor > 2:
            v_lines = v_lines[::skip_n]
            h_lines = h_lines[::skip_n]

        thick = []
        thin = []

        step = UI.graph.grid.step
        mod = 9 - (math.ceil(rect.top() / step) % 10)
        for i, line in enumerate(h_lines):
            if i % 10 == mod:
                thick.append(line)
            else:
                thin.append(line)

        # Two separate enumerations as the two lists will not always
        # be of the same size.
        # Will have to find something better !
        mod = 9 - (math.ceil(rect.left() / step) % 10)
        for i, line in enumerate(v_lines):
            if i % 10 == mod:
                thick.append(line)
            else:
                thin.append(line)

        return thin, thick

    def _get_base_lines(self, rect):
        """Return horizontal and vertical lines of the grid.

        :param rect: Area to cover with lines.
        :type rect: PySide.QtCore.QRectF
        :rtype: tuple(list(PySide.QtCore.QLine), list(PySide.QtCore.QLine))
        """
        step = UI.graph.grid.step
        top = rect.top() - (rect.top() % step)
        bottom = rect.bottom()
        left = rect.left() - (rect.left() % step)
        right = rect.right()

        h_lines = []
        v_lines = []

        x = left
        while x <= right:
            line = _qtcore.QLine(x, top, x, bottom)
            v_lines.append(line)
            x += step

        y = top
        while y <= bottom:
            line = _qtcore.QLine(left, y, right, y)
            h_lines.append(line)
            y += step

        return h_lines, v_lines

    def refresh(self):
        """Force the update of this view."""
        self.scene().update(
            self.viewport().rect().adjusted(-100, -100, 200, 200)
        )
