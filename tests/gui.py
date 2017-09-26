import sys
import os


kukulkan = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py_kukulkan = os.path.join(kukulkan, 'python')


sys.path.append(py_kukulkan)


import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.api.window


def main():
    app = _qt.QApplication(sys.argv)

    window = kukulkan.gui.api.window.GraphWindow()
    jong = window.scene.add_node('jong')
    jonhy = window.scene.add_node('johny')
    rouleau = jong.add_attribute('rouleau_de_printemps')
    autre = jonhy.add_attribute('autre_chose')
    rouleau.is_output = True
    rouleau.is_input = False
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
