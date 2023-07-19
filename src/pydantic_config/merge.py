from copy import deepcopy


def deep_merge(base: dict, nxt: dict, unique: bool = True) -> dict:
    """
    Merges nested dictionaries.

    Parameters
    ----------
    base: dict
        The base dictionary to merge into
    nxt: dict
        The dictionary to merge into base
    unique: bool
        This determines the behavior when merging list values. Lists are appended together which could result
        in duplicate values.  To avoid duplicates set this value to True.

    """
    result = deepcopy(base)

    for key, value in nxt.items():
        if isinstance(result.get(key), dict) and isinstance(value, dict):
            result[key] = deep_merge(result.get(key), value)
        elif isinstance(result.get(key), list) and isinstance(value, list):
            if unique:
                result[key] = result.get(key) + [i for i in deepcopy(value) if i not in set(result.get(key))]
            else:
                result[key] = result.get(key) + deepcopy(value)
        else:
            result[key] = deepcopy(value)
    return result