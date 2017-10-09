import sys
import os


kukulkan_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py_kukulkan = os.path.join(kukulkan_path, 'python')


sys.path.append(py_kukulkan)


import kukulkan.gui.qt.QtGui as _qt
import kukulkan.gui.api.window


def main():
    app = _qt.QApplication(sys.argv)

    window = kukulkan.gui.api.window.GraphWindow()


    node1 = window.scene.add_node('Node1')
    node1.add_attribute(
        name='Integer',
        attribute_type='integer',
        plug_type='output'
    )
    node1.add_attribute(
        name='Float',
        attribute_type='float',
        plug_type='output'
    )
    node1.add_attribute(
        name='Boolean',
        attribute_type='boolean',
        plug_type='output'
    )
    node1.add_attribute(
        name='String',
        attribute_type='string',
        plug_type='output'
    )
    node1.add_attribute(
        name='Enum',
        attribute_type='enum',
        plug_type='output'
    )

    node2 = window.scene.add_node('Node2')
    node2.add_attribute(
        name='Integer',
        attribute_type='integer',
        plug_type='input'
    )
    node2.add_attribute(
        name='Float',
        attribute_type='float',
        plug_type='input'
    )
    node2.add_attribute(
        name='Boolean',
        attribute_type='boolean',
        plug_type='input'
    )
    node2.add_attribute(
        name='String',
        attribute_type='string',
        plug_type='input'
    )
    node2.add_attribute(
        name='Enum',
        attribute_type='enum',
        plug_type='input'
    )

    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
