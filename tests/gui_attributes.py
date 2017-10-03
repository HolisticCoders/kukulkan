
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
    attr1 = node1.add_attribute(
        'Float1',
        _attributes.FloatAttribute,
    )
    attr1.is_input = False
    attr2 = node1.add_attribute(
        'Float2',
        _attributes.FloatAttribute,
    )
    attr2.is_output = False

    window.show()

    sys.exit(app.exec_())

def add_node(window, name):

    attr2 = node1.add_attribute(
        'Float',
        _attributes.FloatAttribute,
    )
    attr3 = node1.add_attribute(
        'Int',
        _attributes.IntAttribute,
    )
    attr4 = node1.add_attribute(
        'Bool',
        _attributes.BoolAttribute,
    )
    attr5 = node1.add_attribute(
        'Enum',
        _attributes.EnumAttribute,
    )


if __name__ == '__main__':
    main()
