"""Handling of user defined configurations."""
import cson
import os


_CONFIG_FILE_EXT = '.cson'
_USER_ENV_VAR_PREFIX = 'KUKULKAN_CONFIG'
_ROOT_TYPES = [
    'default',
    'user',
]


def get_env_var_key(name):
    """Return the name of the environment variable used by this configuration.

    For example, when "ui" is passed, it should return the name of the
    environment variable containing the path to the user "ui.cson" file.

    :param str name: Name of the configuration file or folder.
    :rtype: str
    """
    return '_'.join([_USER_ENV_VAR_PREFIX, name.upper()])


def get_default_folder():
    """Return the default configuration folder.

    :rtype: str
    """
    return os.path.join(os.path.dirname(__file__), 'default')


def get_user_folder():
    """Return the user configuration folder.

    By default, return "~/kukulkan/config"

    Users can edit this path by setting a "KUKULKAN_CONFIG" environment
    variable containing the path to their configuration folder.

    :rtype: str
    """
    home = os.environ.get('HOME', os.path.expanduser('~'))
    return os.path.join(home, 'kukulkan', 'config')


def get_root_folders():
    """Return all configuration folders.

    This include the default one and all user ones.

    :rtype: list(str)
    """
    content = globals()
    getters = []
    for root in _ROOT_TYPES:
        getter_name = 'get_{}_folder'.format(root)
        getter = content.get(getter_name, None)
        if callable(getter):
            getters.append(getter)
    return [g() for g in getters]


def get_configuration_path(
    name,
    root='default',
    config_type=None,
    candidate=False,
):
    """Return a configuration file or folder path.

    The ``name`` argument is the name of the file or folder to get.

    By default, this function will return default configuration
    files and folder, if you want user specific configuration
    set the ``root`` argument to "user".

    If you want to ensure `get_configuration_path` can only return
    a file, you can set the ``config_type`` argument to "file".
    For folders, user the "folder" value.

    If no configuration file or folder is found, return `None`.

    If ``candidate`` argument is set to `True`, then no check is done
    to ensure the folder or file exists.

    :param str name: Name of the configuration file or folder.
    :param str root: Either "default", "user" or any root type available.
    :param str config_type: Force "file" or "folder" look-up.
    :rtype: str or None
    """
    if root == 'user':
        key = get_env_var_key(name)
        if key in os.environ:
            path = os.environ[key]
        else:
            path = os.path.join(get_user_folder(), name)
    else:
        path = os.path.join(get_default_folder(), name)

    # Folder selection
    # Check if this is a folder.
    if config_type == 'folder':
        if candidate:
            return path
    elif config_type is None:
        if os.path.isdir(path):
            return path

    # File selection
    if config_type is None or config_type == 'file':

        # If not, ensure it has the configuration file extension first,
        # then check if it exists.
        if not path.endswith(_CONFIG_FILE_EXT):
            path += _CONFIG_FILE_EXT

        if candidate:
            return path

        if os.path.isfile(path):
            return path

    # No user configuration for this setting.
    return None


def get_configuration_folders(name, candidate=False):
    """Return all folders for the specified setting.

    ``name`` argument should refer to an existing setting folder,
    for example, "themes".

    By default, the default folder is returned.
    If a user configuration folder also exists, it is appended to the
    list.

    If ``name`` does not correspond to any setting, return `None`.

    If ``candidate`` argument is set to `True`, then no check is done
    to ensure the folders exists.

    :param str name: Name of the configuration folder.
    :rtype: list(str) or None
    """
    folders = []
    for root in _ROOT_TYPES:
        folder = get_configuration_path(
            name,
            root,
            'folder',
            candidate,
        )
        if not folder:
            continue

    return folders or None


def get_configuration_files(name, folder=None, candidate=False):
    """Return all configuration files for this setting.

    For example, ``get_configuration_files('ui')`` will return the default
    ``ui.cson`` file and the user one if any.

    You can specify a ``folder`` name to look for this configuration
    file in a configuration folder instead of the root folder.

    If ``name`` does not correspond to any setting, return `None`.

    If ``folder`` does not correspond to any setting, also return `None`.

    If ``candidate`` argument is set to `True`, then no check is done
    to ensure the folders exists.

    :param str name: Name of the configuration file.
    :param str folder: Optional name of a configuration sub-folder.
    :rtype: list(str) or None
    """
    if folder is None:
        folders = get_root_folders()
    else:
        folders = get_configuration_folders(folder, candidate)

    if not folders and not candidate:
        return None
    elif not folders:
        folders = []

    if not name.endswith(_CONFIG_FILE_EXT):
        name += _CONFIG_FILE_EXT

    configs = []
    for folder in folders:
        path = os.path.join(folder, name)
        if not os.path.isfile(path) and not candidate:
            continue
        configs.append(path)

    if not configs and not candidate:
        return None

    return configs


def get_configuration_file_data(name, folder=None, candidate=False):
    """Return the content of a configuration file data.

    You can specify a ``folder`` name to look for this configuration
    file in a configuration folder instead of the root folder.

    If ``name`` does not correspond to any setting, return `None`.

    If ``folder`` does not correspond to any setting, also return `None`.

    If ``candidate`` argument is set to `True`, then no check is done
    to ensure the folders exists.

    :param str name: Name of the configuration file.
    :param str folder: Optional name of a configuration sub-folder.
    :rtype: dict or None
    """
    configs = get_configuration_files(name, folder, candidate)

    if not configs and not candidate:
        return None

    data = {}
    for path in configs:
        if not os.path.isfile(path):
            continue
        with open(path, 'r') as fh:
            data.update(cson.load(fh))

    return data


def get_configuration_folder_choices(name, candidate=False):
    """Return all choices available in a configuration folder.

    This include default and user configurations.

    If ``name`` does not correspond to any folder, return `None`.

    If ``candidate`` argument is set to `True`, then no check is done
    to ensure the folders exists.

    :param str name: Name of the configuration folder.
    :rtype: list(str) or None
    """
    folders = get_configuration_folders(name, candidate)

    if not folders and not candidate:
        return None

    files = []
    for folder in folders:
        if not os.path.isdir(folder):
            continue
        content = os.listdir(folder)
        for file_name in content:
            if not file_name.endswith(_CONFIG_FILE_EXT):
                continue
            if file_name in files:
                continue
            files.append(file_name)

    return files
