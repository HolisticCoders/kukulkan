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


    if_node = window.scene.add_node('If')
    if_node.add_attribute(
        name='Condition',
        attribute_type='boolean',
        plug_type='input',
    )
    if_node.add_attribute(
        name='If True',
        attribute_type='message',
        plug_type='output',
    )
    if_node.add_attribute(
        name='If False',
        attribute_type='message',
        plug_type='output',
    )

    condition_node = window.scene.add_node('Condition')
    condition_node.add_attribute(
        name='Input1',
        attribute_type='integer',
        plug_type='input',
    )
    condition_node.add_attribute(
        name='Input2',
        attribute_type='integer',
        plug_type='input',
    )
    comparator = condition_node.add_attribute(
        name='Comparator',
        attribute_type='enum',
        plug_type='input',
    )
    comparator.base_widget.widget().widget.addItem('=')
    comparator.base_widget.widget().widget.addItem('<')
    comparator.base_widget.widget().widget.addItem('>')
    comparator.base_widget.widget().widget.addItem('<=')
    comparator.base_widget.widget().widget.addItem('>=')

    condition_node.add_attribute(
        name='output',
        attribute_type='boolean',
        plug_type='output',
    )

    for_node = window.scene.add_node('For Loop')
    for_node.add_attribute(
        name='N',
        attribute_type='integer',
        plug_type='input',
    )
    for_node.add_attribute(
        name='Do',
        attribute_type='message',
        plug_type='output',
    )
    for_node.add_attribute(
        name='Then',
        attribute_type='message',
        plug_type='output',
    )

    window.show()

    sys.exit(app.exec_())



if __name__ == '__main__':
    main()