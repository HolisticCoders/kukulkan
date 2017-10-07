"""A simple publisher-observer implementation for event handling."""

import logging

from collections import defaultdict


log = logging.getLogger(__name__)
publishers = defaultdict(list)


def subscribe(func, name):
    """Subscribe to a publisher.

    :param func: Callable subscribing.
    :param name: Name of the publisher to observe.
    :type func: callable
    :type name: str
    """
    publishers[name].append(func)
    log.info('{} subscribed to {}.'.format(func.__name__, name))


def notify(name, *args, **kwargs):
    """Notify all observers.

    :param name: Name of the publisher emitting.
    :type name: str
    """
    if name not in publishers:
        return
    log.info('Emitted {}:'.format(name))
    for func in publishers[name]:
        func(*args, **kwargs)
        log.info('\t{} was notified.'.format(func.__name__))
