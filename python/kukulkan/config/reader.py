import os
import threading
import time

import kukulkan.events
from kukulkan.config.collector import (
    get_configuration_files,
    get_configuration_file_data,
)


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

    :param str name: Name of the configuration file.
    :param str folder: Optional name of a configuration sub-folder.
    :raise ValueError: When ``name`` does not refer to a valid
                       configuration file name.
    """

    def __init__(self, name, folder=None):
        self._assert_configuration_exists(name, folder)
        self.name = name
        self.folder = folder
        self.paths = get_configuration_files(name)
        self.raw_data = {}
        self.data = Root()
        self.read()
        self.watchers = []
        self._setup_watchers()
        event_name = 'config.{}.changed'.format(self.name)
        kukulkan.events.subscribe(self.read, event_name)

    def read(self):
        """Read the configuration file and update this reader data."""
        self.raw_data = get_configuration_file_data(
            self.name,
            self.folder,
        )
        self._visit_raw_data(self.raw_data)

    def __getattr__(self, name):
        if name in self.data.children:
            return self.data.children[name]
        err = 'ConfigReader object has no attribute {}.'.format(name)
        raise AttributeError(err)

    def _assert_configuration_exists(self, name, folder):
        """Ensure ``name`` corresponds to a setting file.

        :param str name: Name of the configuration file.
        :param str folder: Optional name of a configuration
                           sub-folder.
        :raise ValueError: When ``name`` does not refer to a
                           valid configuration file name.
        """
        if not get_configuration_files(name, folder):
            err = (
                '``name`` argument should be '
                'a valid configuration name !'
            )
            raise ValueError(err)

    def _setup_watchers(self):
        """Create `FileWatcher` to keep track of changes."""
        for path in self.paths:
            watcher = FileWatcher(self.name, path)
            watcher.setDaemon(True)
            watcher.start()
            self.watchers.append(watcher)

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
            raise AttributeError(
                'Item object has no attribute {}.'.format(name)
            )

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


class Root(Item):
    """A `ConfigReader` root."""

    def __init__(self):
        self.parent = None
        self.value = self.children = {}
