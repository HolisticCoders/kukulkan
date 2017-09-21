import sys
import os


kukulkan = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py_kukulkan = os.path.join(kukulkan, 'python')


sys.path.append(py_kukulkan)


import autorig.gui.qt.QtGui as _qt
import autorig.gui.jong.window
import autorig.gui.jong.node


def main():
    app = _qt.QApplication(sys.argv)

    window = autorig.gui.jong.window.GraphWindow()
    node = window.scene.add_node('jong')
    node.add_attribute('myAttr')
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
