import sys
import os


kukulkan = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py_kukulkan = os.path.join(kukulkan, 'python')


sys.path.append(py_kukulkan)


import autorig.amate.api


def test_amate_types():
    graph = autorig.amate.api.Graph()


def test_database():
    graph = autorig.amate.api.Graph()
    print 'Built-in database path:', graph.db_dev()
    print 'User database path:', graph.db_user()
    print 'Built-in database content:', graph.db_data_dev()
    print 'User database content:', graph.db_data_user()
    print 'Database data:', graph.db_data()


if __name__ == '__main__':
    test_amate_types()
    test_database()
