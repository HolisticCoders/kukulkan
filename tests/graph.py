import os
import random
import sys


kukulkan = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py_kukulkan = os.path.join(kukulkan, 'python')


sys.path.append(py_kukulkan)


import autorig.graph.api
import autorig.graph.nodes.transform


def main():
    graph = autorig.graph.api.Graph()
    trs1 = autorig.graph.nodes.transform.Transform('trs1')
    trs2 = autorig.graph.nodes.transform.Transform('trs2')
    trs3 = autorig.graph.nodes.transform.Transform('trs3')
    trs4 = autorig.graph.nodes.transform.Transform('trs4')
    trs5 = autorig.graph.nodes.transform.Transform('trs5')

    def iter_nodes():
        yield trs1
        yield trs2
        yield trs3
        yield trs4
        yield trs5

    def get_matrix_rand():
        matrix = [[0] * 4 for _ in xrange(4)]
        for row in xrange(4):
            for column in xrange(4):
                r = int(random.uniform(-10, 10))
                matrix[row][column] = r
        return matrix

    for node in iter_nodes():
        graph.add_node(node)

    trs2.xform.connect(trs3.xform)

    print graph

    for node in iter_nodes():
        try:
            node.xform.set(get_matrix_rand())
        except AttributeError:
            print 'Connected, could not be set.'
        print node, node.xform, node.xform.get()


if __name__ == '__main__':
    main()
