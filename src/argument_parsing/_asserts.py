"""
Contains common assert wrappers.
"""


def assert_is_not_none(instance, error=None):
    """
    Asserts that the instance is of the expected class_info type,
    otherwise, a TypeError with the specified error is raised.

    Args:
        instance (object): The instance to check.
        error (str): The description of the error.

    Raises:
        TypeError: The specified instance is None.
    """
    if instance is None:
        if error is None:
            error = '{instance} cannot be None.'.format(instance=instance)
        raise TypeError(error)


def assert_has_length(iterable: list):
    """
    Asserts that the list has at least 1 item.

    Remarks:
        This also works with iterators without traversing the entire iterable.

    Args:
        iterable:
            The list to check.

    Raises:
        ValueError:
            The iterable does not have at least 1 item.
    """
    has_any = any(iterable)
    if not has_any:
        raise ValueError('The iterable must have at least 1 item.')
