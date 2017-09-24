
import sys
import os


kukulkan = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py_kukulkan = os.path.join(kukulkan, 'python')


sys.path.append(py_kukulkan)


import autorig.gui.qt.QtGui as _qt
import autorig.gui.api.window
import autorig.gui.library.attributes as _attributes


def main():
    app = _qt.QApplication(sys.argv)

    window = autorig.gui.api.window.GraphWindow()
    node1 = window.scene.add_node('node1')
    node2 = window.scene.add_node('node2')
    attribute = node1.add_attribute('FloatAttr', _attributes.FloatAttribute)
    attribute = node2.add_attribute('IntAttr', _attributes.IntAttribute)
    attribute.is_output = True
    attribute.is_input = False
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
