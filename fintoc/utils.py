"""
utils.py
========

A module with a handful of run-of-the-mill utilities.
And they're here to make this codebase more readable.
"""

import itertools


fieldsubs = ("id", "id_"), ("type", "type_")


def flatten(sequence):
    """
    Get a flat list out of a list of lists.
    """

    return list(itertools.chain(*sequence))


def pick(dict_, key):
    """
    If the key exists, you will get that key-value pair.
    And if it doesn't, well... you'll get an empty dict.
    Better luck next time!

    >>> test = {"spam": 42, "ham": "spam"}
    >>> pick(test, "ham")
    {"ham": "spam"}
    >>> pick(test, "eggs")
    {}
    """

    return dict_.get(key, {}) and {key: dict_.get(key)}


def pluralize(amount: int, noun: str, *, suffix: str = "s") -> str:
    """
    Get a pluralized noun with its appropriate quantifier.
    """

    quantifier = amount or "no"
    return f"{quantifier} {noun if amount == 1 else noun + suffix}"


def rename_keys(dist, keys):
    """
    Rename all the dictionary keys *in-place* inside a *dist*,
    which is a nested structure that could be a dict or a list.
    Hence, I named it as dist... which is much better than lict.

    >>> test = {"spam": 42, "ham": "spam", "bacon": {"spam": -1}}
    >>> rename_keys(test, ("spam", "eggs"))
    {"eggs": 42, "ham": "spam", "bacon": {"eggs": -1}}
    """

    if isinstance(dist, list):
        for item in dist:
            rename_keys(item, keys)

    elif isinstance(dist, dict):
        oldkey, newkey = keys
        if oldkey in dist:
            dist[newkey] = dist.pop(oldkey)
        for value in dist.values():
            rename_keys(value, keys)

    return dist


def snake_to_pascal(name: str) -> str:
    """
    Transform a snake-cased name to its pascal-cased version.

    >>> snake_to_pascal("this_example_should_be_good_enough")
    "ThisExampleShouldBeGoodEnough"
    """

    return "".join(word.title() for word in name.split("_"))
