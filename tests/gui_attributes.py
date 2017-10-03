
import sys
import os


kukulkan_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py_kukulkan = os.path.join(kukulkan_path, 'python')


sys.path.append(py_kukulkan)


import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.api.window
import kukulkan.gui.library.attributes as _attributes


def main():
    app = _qt.QApplication(sys.argv)

    window = kukulkan.gui.api.window.GraphWindow()


    node1 = window.scene.add_node('node1')
    node1.add_attribute(
        'Float1',
        _attributes.Float,
        'input'
    )
    node1.add_attribute(
        'Float2',
        _attributes.Float,
        'output'
    )

    node2 = window.scene.add_node('node2')
    node1.add_attribute(
        'Float1',
        _attributes.Float,
        'input'
    )
    node1.add_attribute(
        'Float2',
        _attributes.Float,
        'output'
    )

    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
