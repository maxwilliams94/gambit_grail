"""
Utility Functions
"""
from collections.abc import Iterable, Iterator


def cast_singleton(_it: Iterable):
    """
    Cast an iterable to a single value if possible, otherwise return as a list
    """
    if isinstance(_it, Iterator):
        array = list(_it)
    else:
        array = _it

    if len(array) == 1:
        return array[0]

    return array 