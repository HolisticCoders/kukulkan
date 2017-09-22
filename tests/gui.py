import sys
import os


kukulkan = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py_kukulkan = os.path.join(kukulkan, 'python')


sys.path.append(py_kukulkan)


import autorig.gui.qt.QtGui as _qt
import autorig.gui.api.window


def main():
    app = _qt.QApplication(sys.argv)

    window = autorig.gui.api.window.GraphWindow()
    jong = window.scene.add_node('jong')
    jonhy = window.scene.add_node('johny')
    jong.add_attribute('rouleau_de_printemps')
    jonhy.add_attribute('autre_chose')
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
