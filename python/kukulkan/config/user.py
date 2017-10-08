"""Handling of user defined configurations."""


_USER_ENV_VAR_PREFIX = 'KUKULKAN_CONFIG'


def get_env_var_key(name):
    """Return the name of the environment variable used by this configuration.

    For example, when "ui" is passed, it should return the name of the
    environment variable containing the path to the user "ui.cson" file.

    :param str name: Name of the configuration file or folder.
    :rtype: str
    """
    return '_'.join([_USER_ENV_VAR_PREFIX, name.upper()])
