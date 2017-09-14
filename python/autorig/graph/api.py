import uuid
from collections import MutableSequence
from functools import wraps

is_dirty = False


def set_dirty(f):
    """Set the current graph dirty.
    """
    global is_dirty

    @wraps(f)
    def inner(*args, **kwargs):
        return f(*args, **kwargs)

    is_dirty = True

    return inner


def set_clean(f):
    """Set the current graph clean.
    """
    global is_dirty

    @wraps(f)
    def inner(*args, **kwargs):
        return f(*args, **kwargs)

    is_dirty = False

    return inner


class Unique(object):

    def __init__(self):
        self.uuid = uuid.uuid4()


class Graph(Unique):
    """A `Graph` containing `Node` items.
    """

    def __init__(self):
        super(Graph, self).__init__()
        self.nodes = {}

    def __str__(self):
        return '\n'.join(map(str, self.nodes.values()))

    def add_node(self, node):
        """Add an existing node to this graph.

        :param Node node: `Node` to add.
        :return: The node added
        :rtype: Node
        """
        self.nodes[node.uuid] = node

    def remove_node(self, node):
        """Remove a node from the graph.

        :param Node node: `Node` or uuid of the node to remove.

        :return: The node removed.
        :rtype: Node
        """
        if isinstance(node, Node):
            node = node.uuid
        if uuid not in self.nodes:
            raise KeyError('Node {} does not exist.'.format(node))
        return self.nodes.pop(uuid)


class Node(Unique):
    """A `Node` containing `Attribute` items.
    """

    attributes = {}

    def __init__(self, name):
        super(Node, self).__init__()
        self._generate_attributes()
        self.name = name

    def __str__(self):
        return str(self.name)

    def _generate_attributes(self):
        """Generate built-in attributes of this `Node`.
        """
        for name, attribute_class in self.attributes.iteritems():
            attribute = attribute_class(name, self)
            setattr(self, name, attribute)

    def run(self):
        """Method executed when the state of the graph changes.
        """


class Attribute(Unique):
    """A `Node` `Attribute`.
    """

    default_value = None

    def __init__(self, name, node):
        super(Attribute, self).__init__()
        self.inputs = {}
        self.outputs = {}
        self.value = self.default_value
        self.node = node
        self.name = name

    def __str__(self):
        return '.'.join(map(str, [self.node, self.name]))

    def validate_value(self, value):
        """Validate and possibly modify the value to set on this `Attribute`.

        This is a mean to convert incoming values before setting them
        on the `Attribute`.

        For exemple, this method could cast any input value to integers.

        This method has to return the final, validated value or raise a
        `ValueError`.

        :param value: Incoming value to set.
        :return: The correct value
        :raise ValueError: If the value cannot be validated.
        """
        return value

    def get(self):
        """Return the value of this `Attribute`.
        """
        if self.inputs:
            return self.inputs.values()[0].get()
        return self.value

    def set(self, value):
        """Set the value of this `Attribute`.

        This method will first call `Attribute.validate_value`
        to ensure the value set corresponds to the kind of data
        this `Attribute` expects.

        :param value: Value to set on this `Attribute`.
        """
        if self.inputs:
            err = 'Attribute {} has an incoming connection, cannot be set.'
            raise AttributeError(err.format(self))
        value = self.validate_value(value)
        self.value = value

    def connect(self, other):
        """Connect this `Attribute` to another one.

        This `Attribute` output will go in the other `Attribute` input.

        :param Attribute other: Attribute to connect to.
        """
        self.outputs[other.uuid] = other
        other.inputs[self.uuid] = self

    def disconnect(self, other):
        """Disconnect this `Attribute` from another one.

        This `Attribute` output will be disconnected from the other
        `Attribute` input.

        :param Attribute other: Attribute to disconnect from.
        """
        self.outputs.pop(other.uuid)
        other.inputs.pop(self.uuid)


class AttributeList(Unique, MutableSequence):

    def __init__(self, name, node):
        super(AttributeList, self).__init__()
        self.attributes = []
        self.node = node
        self.name = name

    def __str__(self):
        return '.'.join([self.node, self.name])

    def get(self):
        """Return the list of `Attribute` values contained."""
        return [a.get() for a in self]

    def set(self, values):
        """Set the values of the `Attribute` items contained.

        You must specify an iterable of values, and attributes will
        be set beginning by the first added.

        If there is more values than attributes, then the remaining
        values will be of no use.

        If there is more attributes, then the last n attributes will
        not be set.

        :param list values: Values to set on the attributes.
        """
        for attribute, value in zip(self, values):
            attribute.set(value)

    # MutableSequence implementation
    # ------------------------------
    def __getitem__(self, index):
        return self.attributes[index]

    def __setitem__(self, index, value):
        self.attributes[index] = value

    def __delitem__(self, index):
        del self.attributes[index]

    def __len__(self):
        return len(self.attributes)

    def insert(self, index, value):
        """Insert a new attribute at the given index."""
        return self.attributes.insert(index, value)
