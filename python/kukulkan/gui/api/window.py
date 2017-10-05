import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.api.graph as _graph


class GraphWindow(_qt.QMainWindow):
    """A node editor window."""

    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        self.build()

    def build(self):
        self.view = _graph.GraphView()
        self.scene = _graph.Graph()
        self.view.setScene(self.scene)
        self.view.setRenderHints(_qt.QPainter.Antialiasing)
        self.setCentralWidget(self.view)
