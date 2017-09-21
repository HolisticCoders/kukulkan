import autorig.gui.qt.QtGui as _qt
import autorig.gui.jong.graph as _graph


class GraphWindow(_qt.QMainWindow):
    """A node editor window."""

    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        self.build()

    def build(self):
        self.view = _qt.QGraphicsView()
        self.scene = _graph.Graph()
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)
