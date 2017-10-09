import os

from .collector import get_default_folder
from .reader import ConfigReader
from .watchers import FolderWatcher


def setup():
    """Setup Kukulkan configuration.

    Gather all configuration files and associate a `FileWatcher`.
    Same for folders, with `FolderWatcher` objects.
    """
    root = get_default_folder()
    _walk_folder(root)


def _walk_folder(root):
    for name in os.listdir(root):
        path = os.path.join(root, name)
        if os.path.isfile(path):
            key = name.split('.')[0]
            reader = ConfigReader(key)
            globals()[key.upper()] = reader
        elif os.path.isdir(path):
            kukulkan.config.watchers.FolderWatcher(name, path)
            _walk_folder(path)


setup()
