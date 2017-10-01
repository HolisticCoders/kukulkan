
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
    node1 = window.scene.add_node('Float')
    node2 = window.scene.add_node('Int')
    node3 = window.scene.add_node('Bool')
    node4 = window.scene.add_node('String')
    node5 = window.scene.add_node('Enum')

    attr1 = node1.add_attribute('FloatAttr', _attributes.FloatAttribute)
    attr2 = node2.add_attribute('IntAttr', _attributes.IntAttribute)
    attr3 = node3.add_attribute('BoolAttr', _attributes.BoolAttribute)
    attr4 = node4.add_attribute('StringAttr', _attributes.StringAttribute)
    attr5 = node5.add_attribute('EnumAttr', _attributes.EnumAttribute)

    attr1.is_input=False
    attr1.is_output=False
    attr2.is_output=False
    attr3.is_input=False
    attr4.is_output=False
    attr5.is_input=False

    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
