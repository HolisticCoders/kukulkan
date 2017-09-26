
import sys
import os


kukulkan = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py_kukulkan = os.path.join(kukulkan, 'python')


sys.path.append(py_kukulkan)


import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.api.window
import kukulkan.gui.library.attributes as _attributes


def main():
    app = _qt.QApplication(sys.argv)

    window = kukulkan.gui.api.window.GraphWindow()
    node1 = window.scene.add_node('Floats')
    node2 = window.scene.add_node('Ints')
    node3 = window.scene.add_node('Bools')
    node4 = window.scene.add_node('Strings')
    node5 = window.scene.add_node('Enums')

    for i in range(25):
        node1.add_attribute('FloatAttr' + str(i), _attributes.FloatAttribute)
        node2.add_attribute('IntAttr' + str(i), _attributes.IntAttribute)
        node3.add_attribute('BoolAttr' + str(i), _attributes.BoolAttribute)
        node4.add_attribute('StringAttr' + str(i), _attributes.StringAttribute)
        node5.add_attribute('EnumAttr' + str(i), _attributes.EnumAttribute)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
