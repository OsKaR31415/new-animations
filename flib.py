
def flatten(lists: list[list]):
    """Recursively flatten nested lists.
    Examples:
        >>> flatten([1, [2, 3], 4])
        [1, 2, 3, 4]
        >>> flatten([1, 2, [3, [4, 5, 6], 7, [8, 9]], 10])  # any depth
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> flatten([1, 2, (3, 4, [5, 6], (7, 8)), 9])  # works with tuples
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    flattened = []
    for elt in lists:
        if isinstance(elt, (list, tuple)):
            flattened.extend(flatten(elt))
        else:
            flattened.append(elt)
    return list(flattened)




