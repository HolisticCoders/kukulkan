"""Amate API module, introducing graph and nodes api.
"""
from collections import OrderedDict, MutableMapping
import json
import logging
import os


log = logging.getLogger(__name__)

child_types = {
    'Graph': 'Node',
    'Node': 'Attribute',
}


class AmateObject(MutableMapping):

    default_db = {
        'graph': {},
        'node': {},
        'attribute': {},
    }
    amate_type = None

    def __init__(self):
        super(AmateObject, self).__init__()
        self.data = {}
        self.data['children'] = OrderedDict()

    @staticmethod
    def db_user():
        """Return the path to the Amate user database."""
        return os.environ.get('AMATE_DB')

    @staticmethod
    def db_dev():
        """Return the path to the Amate built-in database."""
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.json')

    @staticmethod
    def db_data_dev():
        """Return all Amate built-in data."""
        db_dev = AmateObject.db_dev()
        if not (db_dev and os.path.isfile(db_dev)):
            data = AmateObject.default_db
        else:
            with open(db_dev, 'r') as fh:
                data = json.load(fh, object_pairs_hook=OrderedDict)
        return data

    @staticmethod
    def db_data_user():
        """Return all Amate user data."""
        db_user = AmateObject.db_user()
        if not (db_user and os.path.isfile(db_user)):
            data = {}
        else:
            with open(db_user, 'r') as fh:
                data = json.load(fh, object_pairs_hook=OrderedDict)
        return data

    @staticmethod
    def db_data():
        """Return all Amate database data."""
        data = AmateObject.db_data_dev()
        data.update(AmateObject.db_data_user())
        return data

    def data_to_str(self):
        """Return this object's data converted to string."""
        data = self.data
        children = data['children']
        serializable = {}
        for name, child in children.iteritems():
            serializable[name] = child.__class__.__name__
        data['children'] = serializable
        return data

    def save(self, name, db_type='user'):
        """Save this Amate object to database.

        There is two databases for Amate:

            * A built-in database containing default types of Amate
              objects

            * A user database that Amate users can manage to add their
              own types of Amate objects (graphs, nodes, attributes...)

        By defaut, saving an Amate object saves to the user database.
        If you want to modify the Amate package database, just provide
        a 'dev' value to the 'db_type' argument of this method.

        :param str db_type: Database into which the object should be saved.
        """
        if db_type != 'dev' and not AmateObject.db_user():
            error = 'No Amate user database specified.\n'
            error += 'Is AMATE_DB environment variable set ?'
            raise FileNotFoundError(error)

        db = self.db_dev() if db_type == 'dev' else self.db_user()

        if os.path.isfile(db):
            with open(db, 'r') as fh:
                data = json.load(fh, object_pairs_hook=OrderedDict)
        else:
            data = AmateObject.default_db

        data[self.amate_type][name] = self.data_to_str()

        with open(db, 'w') as fh:
            json.dump(data, fh, indent=4)

    def load(self, name):
        """Load data for this Amate object from database.

        :param str name: Name of the object class to load.
        """
        data = self.db_data()[self.amate_type][name]
        for name, type in data.pop('children', {}).iteritems():
            self.add_child(name, type)
        self.data = data

    def children(self):
        """Return the children of this object.

        :rtype: dict{str: AmateObject}
        """
        return self.data['children']

    def add_child(self, name, type):
        """Add a child to this object.

        :param str name: Name of the created child.
        :param str type: Type of child you want to add.

        :return: The created child.
        :rtype: AmateObject
        """
        if name in self:
            msg = '{} already has a child named {}.'
            raise ValueError(msg.format(self.__class__.__name__, name))
        parent_class = self.__class__.__name__
        if parent_class not in child_types:
            raise AttributeError(parent_class + ' cannot have children.')
        child_class = globals()[child_types[parent_class]]
        child = child_class()
        child.load(type)
        self.data['children'][name] = child
        return child

    def remove_child(self, name):
        """Remove the specified child from this object.

        :raise: KeyError if the child does not exist.
        """
        del self.data['children'][name]

    def __getitem__(self, key):
        return self.data['children'][key]

    def __setitem__(self, key, value):
        self.data['children'][key] = value

    def __delitem__(self, key):
        del self.data['children'][key]

    def __iter__(self):
        yield self.data['children']

    def __len__(self):
        return len(self.data['children'])


class Graph(AmateObject):
    """An Amate scene representation graph.
    """

    amate_type = 'graph'


class Node(AmateObject):
    """A basic Amate node (vertex)."""

    amate_type = 'node'


class Attribute(AmateObject):
    """Attributes found on Amate nodes."""

    amate_type = 'attribute'

    def connect(self, other):
        """Connect this Amate Attribute to another one.

        :param Attribute other: The attribute to drive.
        """
