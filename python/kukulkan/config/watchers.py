import os
import threading
import time

import kukulkan.events


class FileWatcher(threading.Thread):
    """Watch for file changes.

    Also, update the damn application when that happens.

    This watcher notifies the watched file path creation, deletion
    and modification.

    :param name: Name of this `FileWatcher`.
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
            self.last_mtime = self.current_mtime()

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


class FolderWatcher(threading.Thread):
    """Watch for folder changes.

    Also, update the damn application when that happens.

    This watcher notifies watched folder path creation, deletion, and
    child creation and deletion.

    :param name: Name of this `FolderWatcher`.
    :param path: Path to observe.
    :type name: str
    :type path: str
    """

    def __init__(self, name, path):
        super(FolderWatcher, self).__init__()
        self.name = name
        self.path = path
        if not os.path.isdir(path):
            self.exists = False
            self.children = set()
        else:
            self.exists = True
            self.children = set(os.listdir(self.path))

    def run(self):
        """Update the state of the file."""
        while True:
            if self.exists:
                if not os.path.isdir(self.path):
                    # Does not exist anymore.
                    self.exists = False
                    self.folder_deleted()
            else:
                if os.path.isdir(self.path):
                    # Just got created.
                    self.exists = True
                    self.children = os.listdir(self.path)
                    self.folder_created()

            old_children = self.children
            if os.path.isdir(self.path):
                self.children = set(os.listdir(self.path))
            else:
                self.children = set()

            created_children = self.children - old_children
            deleted_children = old_children - self.children

            for child in created_children:
                self.child_created(child)

            for child in deleted_children:
                self.child_deleted(child)

            time.sleep(1)

    def _event_key(self):
        """Return the watched folder event key.

        :rtype: str
        """
        return 'config.' + self.name

    def _child_event_key(self, name):
        """Return the watched child event key.

        :rtype: str
        """
        return 'config.' + '.'.join([self.name, name])

    def folder_deleted(self):
        """Called when the watched folder gets deleted."""
        kukulkan.events.notify(self._event_key() + '.deleted')

    def folder_created(self):
        """Called when the watched folder is created."""
        kukulkan.events.notify(self._event_key() + '.created')

    def child_deleted(self, name):
        """Called when a child file or folder gets deleted.

        Notification sends the created child base name to subscribers.

        :param str name: Name of the deleted child.
        """
        kukulkan.events.notify(self._child_event_key(name) + '.deleted')

    def child_created(self, name):
        """Called when a child file or folder is created.

        Notification sends the created child base name to subscribers.

        :param str name: Name of the created child.
        """
        kukulkan.events.notify(self._child_event_key(name) + '.created')
