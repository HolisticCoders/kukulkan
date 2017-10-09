import os

from .collector import get_default_folder, get_configuration_folder_choices
from .reader import ConfigReader
from .watchers import FolderWatcher


def setup():
    """Setup Kukulkan configuration.

    Gather all configuration files and associate a `FileWatcher`.
    Same for folders, with `FolderWatcher` objects.
    """
    root = get_default_folder()
    for name in os.listdir(root):
        path = os.path.join(root, name)
        if os.path.isfile(path):
            key = name.split('.')[0]
            reader = ConfigReader(key)
            globals()[key.upper()] = reader
            print 'New ConfigReader:', key
        elif os.path.isdir(path):
            FolderWatcher(name, path)
            print 'New FolderWatcher:', name

            choices = get_configuration_folder_choices(name, candidate=True)
            for choice in choices:
                key = choice.split('.')[0]
                reader = ConfigReader(key, folder=name)
                globals()[key.upper()] = reader
                print 'New ConfigReader:', key, name


setup()
