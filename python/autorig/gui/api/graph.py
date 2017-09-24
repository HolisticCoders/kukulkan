import autorig.gui.qt.QtGui as _qt

import autorig.gui.api.node as _node


class Graph(_qt.QGraphicsScene):

    def add_node(self, name):
        node = _node.Node(name)
        self.addItem(node)
        return node