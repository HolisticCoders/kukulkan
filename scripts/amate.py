import sys
import os


kukulkan = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py_kukulkan = os.path.join(kukulkan, 'python')


sys.path.append(py_kukulkan)


import autorig.amate.api


def add_node_type(name, attributes):
    node = autorig.amate.api.Node()
    for a_name, a_type in attributes.iteritems():
        node.add_child(a_name, a_type)
    node.save(name, 'dev')


if __name__ == '__main__':
    nodes = {
        'control': {
            'xform': 'transform',
            'shape': 'shape',
        },
        'transform': {
            'xform': 'transform',
        }
    }
    for name, attributes in nodes.iteritems():
        add_node_type(name, attributes)
