import kukulkan.events
from kukulkan.config.collector import (
    get_configuration_files,
    get_configuration_file_data,
)
from kukulkan.config.watchers import FileWatcher


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
