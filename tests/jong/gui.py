import sys
import os


kukulkan = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
py_kukulkan = os.path.join(kukulkan, 'python')


sys.path.append(py_kukulkan)


import autorig.gui.qt.QtGui as _qt
import autorig.gui.api.window
import autorig.gui.api.attribute


def main():
    app = _qt.QApplication(sys.argv)

    window = autorig.gui.api.window.GraphWindow()
    jong = window.scene.add_node('jong')
    johnny = window.scene.add_node('johnny')

    attr = autorig.gui.api.attribute.Attribute

    rouleau = jong.add_attribute('rouleau_de_printemps', attr)
    autre = johnny.add_attribute('autre_chose', attr)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
