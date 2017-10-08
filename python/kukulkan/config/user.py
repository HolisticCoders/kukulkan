"""Handling of user defined configurations."""
import os


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
