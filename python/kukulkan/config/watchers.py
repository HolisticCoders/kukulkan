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

