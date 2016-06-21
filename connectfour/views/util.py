def get_positive_int(num, name='Number', max_value=None,
                     default_if_blank=None):
    """Convert a string to an int, enforcing that it is positive.

    Raises an error if num is not convertible to a positive int.

    Args:
        num (str): The value to cast to an int.
        name (Optional[str]): A name describing the number (e.g. 'Days'),
            for printing in error messages.
        max_value (Optional[int]): Maximum value that the number can be.
    Returns:
        int: The number cast to an int, if it meets all criteria.
    Raises:
        ValueError: If number is not convertible to an int, if it is
            not positive, or if it exceeds max_value.
    """
    if default_if_blank and len(num) == 0:
        return default_if_blank

    try:
        num = int(num)
    except ValueError:
        raise ValueError('{} must be an integer'.format(name))

    if num <= 0:
        raise ValueError('{} must be positive'.format(name))

    if max_value and num > max_value:
        raise ValueError("{} can't exceed {}".format(name, max_value))

    return num


def get_nonempty_string(s, name='String', max_len=None):
    if not len(s):
        raise ValueError('{} must be non-empty'.format(name))

    if max_len and len(s) > max_len:
        raise ValueError("{} can't exceed {} characters".format(name, max_len))

    return s
