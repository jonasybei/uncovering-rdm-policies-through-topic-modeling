import re

def flatten(lst):
    """
    Recursively flattens a nested list into a single list.

    This function takes a list that may contain nested lists at any level of depth
    and returns a new list with all the elements flattened into a single,
    one-dimensional list, preserving the original order of elements.

    Parameters:
        lst (list): A list that may contain nested lists.

    Returns:
        list: A flattened list with all elements from the input list, in the same order.

    Example:
    nested_list = [1, [2, 3, [4, 5]], [6, [7, 8]], 9]
    flatten(nested_list) = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """

    flat_list = []
    for sublist in lst:
        if isinstance(sublist, list):
            flat_list.extend(flatten(sublist))
        else:
            flat_list.append(sublist)
    return flat_list


def contains_text(text):
    """
    Checks whether a string contains any letters from A-Z or a-z.
    :param text: The string to check.
    :return bool: Whether the string contains any letters from A-Z or a-z.
    """
    return bool(re.search(r'[A-Za-z]', text))