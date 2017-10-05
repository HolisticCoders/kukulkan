import cson
import os
import threading
import time

import kukulkan.events


class FileWatcher(threading.Thread):
    """Watch for file changes.

    Also, update the damn application when that happens.

    :param name: Name of this FileWatcher.
    :param path: Path to observe.
    :type name: str
    :type path: str
    """

    def __init__(self, name, path):
        super(FileWatcher, self).__init__()
        self.name = name
        self.path = path
        if not os.path.isfile(path):
            self.exists = False
            self.last_mtime = 0
        else:
            self.exists = True
            self.last_mtime = os.path.getmtime(path)

    def run(self):
        """Update the state of the file."""
        while True:
            if self.exists:
                if not os.path.isfile(self.path):
                    self.exists = False
                    self.file_deleted()
                elif self.current_mtime() != self.last_mtime:
                    self.last_mtime = self.current_mtime()
                    self.file_changed()
            else:
                if os.path.isfile(self.path):
                    self.exists = True
                    self.file_created()
            time.sleep(1)

    def current_mtime(self):
        return os.path.getmtime(self.path)

    def file_deleted(self):
        """Called when the watched file gets deleted."""
        kukulkan.events.notify('config.' + self.name + '.deleted')

    def file_created(self):
        """Called when the watched file is created."""
        kukulkan.events.notify('config.' + self.name + '.created')

    def file_changed(self):
        """Called when the watched file changes."""
        kukulkan.events.notify('config.' + self.name + '.changed')


class ConfigReader(object):
    """A configuration file reader.

    :param str name: Name of the target configuration file.
    :param str extension: Extension for this configuration file.
    """

    def __init__(self, name, extension='.cson'):
        self.name = name
        self.extension = extension
        self.path = self.resolve_path(name, extension)
        self.watcher = FileWatcher(name, self.path)
        self.raw_data = {}
        self.data = Root()
        if os.path.isfile(self.path):
            self.read()
        self.watcher.setDaemon(True)
        self.watcher.start()
        kukulkan.events.subscribe(self.read, 'config.ui.changed')

    @staticmethod
    def resolve_path(name, extension):
        """Resolve full path for target configuration file name.

        :param str name: Name of the target configuration file.
        :param str extension: Extension for this configuration file.
        :rtype: str
        """
        if not name.endswith(extension):
            name += extension
        return os.path.join(os.path.dirname(__file__), 'default', name)

    def read(self):
        """Read the configuration file and update this reader data."""
        with open(self.path, 'r') as fh:
            self.raw_data = cson.load(fh)
        self._visit_raw_data(self.raw_data)

    def __getattr__(self, name):
        if name in self.data.children:
            return self.data.children[name]
        err = 'ConfigReader object has no attribute {}.'.format(name)
        raise AttributeError(err)

    def _visit_raw_data(self, root, parent=None):
        """Recursively visit a tree."""
        if parent is None:
            parent = self.data
        for key, value in root.iteritems():
            if isinstance(value, dict):
                item = Item(value, parent)
                self._visit_raw_data(value, item)
            else:
                item = value
            parent.children[key] = item


class Item(object):
    """A `ConfigReader` item."""

    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        self.children = {}

    def __getattr__(self, name):
        if name in self.children:
            return self.children[name]
        try:
            return getattr(self.value, name)
        except AttributeError:
            raise AttributeError('Item object has no attribute {}.'.format(name))

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


class Root(Item):
    """A `ConfigReader` root."""

    def __init__(self):
        self.parent = None
        self.value = self.children = {}
