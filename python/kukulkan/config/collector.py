"""Handling of user defined configurations."""
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


def get_configuration_path(name, root='default', config_type=None):
    """Return a configuration file or folder path.

    The ``name`` argument is the name of the file or folder to get.

    By default, this function will return default configuration
    files and folder, if you want user specific configuration
    set the ``root`` argument to "user".

    If you want to ensure `get_configuration_path` can only return
    a file, you can set the ``config_type`` argument to "file".
    For folders, user the "folder" value.

    If no configuration file or folder is found, return `None`.

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
    if config_type is None or config_type == 'folder':
        if os.path.isdir(user_path):
            return user_path

    # File selection
    if config_type is None or config_type == 'file':

        # If not, ensure it has the configuration file extension first,
        # then check if it exists.
        if not user_path.endswith(_CONFIG_FILE_EXT):
        user_path += _CONFIG_FILE_EXT

        if os.path.isfile(user_path):
            return user_path

    # No user configuration for this setting.
    return None


def get_configuration_folders(name):
    """Return all folders for the specified setting.

    ``name`` argument should refer to an existing setting folder,
    for example, "themes".

    By default, the default folder is returned.
    If a user configuration folder also exists, it is appended to the
    list.

    If ``name`` does not correspond to any setting, return `None`.

    :param str name: Name of the configuration folder.
    :rtype: list(str) or None
    """
    folders = []
    for root in _ROOT_TYPES:
        folder = get_configuration_path(name, root, 'folder')
        if not folder:
            continue

    return folders or None


def get_configuration_file_data(name, folder=None):
    """Return the content of a configuration file data.

    You can specify a ``folder`` name to look for this configuration
    file in a configuration folder instead of the root folder.

    If ``name`` does not correspond to any setting, return `None`.

    If ``folder`` does not correspond to any setting, also return `None`.

    :param str name: Name of the configuration file.
    :param str folder: Optional name of a configuration sub-folder.
    :rtype: dict or None
    """
    if folder is None:
        folders = get_root_folders()
    else:
        folders = get_configuration_folders(folder)

    if not folders:
        return None

    if not name.endswith(_CONFIG_FILE_EXT):
        name += _CONFIG_FILE_EXT

    configs = []
    for folder in folders:
        path = os.path.join(folder, name)
        if not os.path.isfile(config):
            continue
        configs.append(config)

    if not configs:
        return None

    data = {}
    for path in configs:
        with open(path, 'r') as fh:
            data.update(cson.load(fh))

    return data


def get_configuration_folder_choices(name):
    """Return all choices available in a configuration folder.

    This include default and user configurations.

    If ``name`` does not correspond to any folder, return `None`.

    :param str name: Name of the configuration folder.
    :rtype: list(str) or None
    """
    folders = get_configuration_folders(name)

    if not folders:
        return None

    files = []
    for folder in folders:
        content = os.listdir(folder)
        for file_name in content:
            if not file_name.endswith(_CONFIG_FILE_EXT):
                continue
            if file_name in files:
                continue
            files.append(file_name)

    return files
