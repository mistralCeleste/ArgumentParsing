"""
Utility functions dealing with iterables, lists, and dictionaries.
"""

from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable, Iterable, Iterator, List, Optional, Tuple, TypeVar
from ._asserts import assert_is_not_none, assert_has_length


def flatten(items, delimiter=' '):
    """
    Flattens a list to a joined text list with the specified delimiter.

    Args:
        items:
            Items to flatten.
        delimiter:
            The delimiter to use when joining the items together.

    Returns:
        A flattened list.
    """
    values = [str(item) for item in items if item != '']
    value = delimiter.join(values)
    return value


def split(
        text: str,
        delimiter: str = ','
) -> List[str]:
    """
    Splits a string of items into a stripped, non-empty list of strings.

    Args:
        text:
            Text to split.
        delimiter:
            Delimiter used to split the text.

    Returns:
        List of stripped, non-empty items split from the text.
    """
    split_items = text.split(delimiter)
    parsed = [item.strip() for item in split_items if item]
    return parsed


def get_first_item(
        iterable: any,
        condition: Callable[[any], bool] = lambda x: True) -> any:
    """
    Gets the first item of an iterable that matches a condition.
    If no condition is specified, then the first item is returned.

    Args:
        iterable:
            The iterable containing the first item to retrieve.
        condition:
            The condition to search for.  By default, this is any item in the iterable.

    Returns:
        The first item from the iterable.

    Raises:
            TypeError:
                iterable is not actually iterable.
            StopIteration:
                The iterable is empty.
    """
    first = next(item for item in iterable if condition(item))
    return first


def get_first_sorted_value(
        array: list,
        key: any,
        reverse: bool = False) -> any:
    """

    Args:
        array:
            The list of values to search within.
        key:
            The key to use for sorting the values.
        reverse:
            A value indicating whether to reverse the order of the sort operation.

    Returns:
        The first value in the sorted list.

    Raises:
        TypeError:
            The iterable is not an iterable type.
        ValueError:
            The array has nothing in it.
    """
    assert_is_not_none(array)
    assert_has_length(array)
    array.sort(key=key, reverse=reverse)
    value = array[0]
    return value


def has_any(iterable: Iterable):
    """
    Gets a value indicating whether the iterable has anything in it.

    Args:
        iterable:
            The iterable to check whether it has anything in it.
    """
    return iterable is not None and any(iterable)


def get_highest_value(
        array: list,
        key: any) -> any:
    """
    Gets the highest value from the list using the specified key.

    Args:
        array:
            The list of values to search within.
        key:
            The key to use for objects in order to determine the highest value.

    Returns:
        The highest value in the list.

    Raises:
        TypeError:
            The iterable is not an iterable type.
        ValueError:
            The array has nothing in it.
    """
    value = get_first_sorted_value(array, key, reverse=True)
    return value


def get_lowest_value(
        array: list,
        key: any) -> any:
    """
    Gets the lowest value from the list using the specified key.

    Args:
        array:
            The list of values to search within.
        key:
            The key to use for objects in order to determine the lowest value.

    Returns:
        The lowest value in the list.

    Raises:
        TypeError:
            The iterable is not an iterable type.
        ValueError:
            The array has nothing in it.
    """
    value = get_first_sorted_value(array, key)
    return value


def aggregate_while(
        items: list,
        start: int = 0,
        condition: Callable[..., bool] = lambda x, y: True,
        *args,
        **kwargs) -> Tuple[list, int]:
    """
    Aggregates a list while the specified condition is True.

    Args:
        items:
            The items to aggregate.
        start:
            The index in the list to start aggregation.
        condition:
            The condition to search for.  By default, this is every item in the list.

    Returns:
        A list containing the items meeting the condition.

    Example:
        foo = [1, 4, 2, 6, 5]
        bar, stop = aggregate_while(foo, condition=lambda aggregate, item: aggregate + item < 7)
        # bar = [1, 4, 2] stop = 3
        bar, stop = aggregate_while(foo, stop, lambda aggregate, item: aggregate + item < 7)
        # bar = [6], stop = 4
    """
    aggregate = []
    index = start
    for item in items[index:]:
        if condition(aggregate, item, *args, **kwargs):
            aggregate.append(item)
            index += 1
        else:
            break
    return aggregate, index


T_Item = TypeVar('T_Item', bound=object)


def unwrap(
        item: T_Item,
        un_wrapper: Callable[[T_Item], Optional[T_Item]]) -> List[T_Item]:
    """
    Unwraps nested objects into a single list containing those objects with the deepest child first.

    Args:
        item:
            The item to unwind.
        un_wrapper:
            The callable used to unwrap the object.

    Returns:
        A list containing the un-wrapped items.
    """
    items = []
    if item is not None:
        child = un_wrapper(item)
        children = unwrap(child, un_wrapper)
        items.extend(children)
        items.append(item)
    return items


def filter_many(
        selector: Callable[[List[str], str], str],
        items: List[str],
        patterns: List[str]) -> Iterator[str]:
    """
    Generator function which yields the names that match one or more of the patterns.

    Args:
        selector:
            selector used to select specific items from the list.
        items:
            Items to select from.
        patterns:
            A pattern used to select specific items from the list of items.

    Yields:
        An item that matches the pattern.
    """
    for pattern in patterns:
        yield from select(selector, items, pattern)


def select(
        selector: Callable[[List[str], str], str],
        items: List[str],
        pattern: str) -> Iterator[str]:
    """
    Selects items from a list that match the selection.

    Args:
        selector: The selector used to determine whether the item meets the condition.
        items: The items to select.
        pattern: The pattern to match for each item.

    Returns:
        An iterator that contains the items matching the selection.
    """
    yield from selector(items, pattern)


def where(
        selector: Callable[[T_Item, any], bool],
        items: List[T_Item],
        *args,
        **kwargs
) -> Iterator[T_Item]:
    """
    Filters a list where the selector is True.

    Args:
        selector: The selector used to determine whether the item meets the condition.
        items: The items to select from.
        *args: Any parameters to pass to the selector after the item.
        **kwargs: Any parameters to pass to the selector after the item.

    Returns:
        An iterator that contains the items matching the selection.
    """
    for item in items:
        selected = selector(item, *args, **kwargs)
        if selected:
            yield item


def foreach(
        items: Iterator[T_Item],
        action: Callable[[T_Item, any], None],
        *args,
        **kwargs
) -> None:
    """
    Runs an action on each of the items in the sequence.

    Args:
        items: The items to perform the action on.
        action: The action to perform on each item.
        *args: Any parameters to add to the action to be performed.
        **kwargs: Any parameters to add to the action to be performed.
    """
    for item in items:
        action(item, *args, **kwargs)


def foreach_async(
        items: Iterator[T_Item],
        action: Callable[[T_Item, any], None],
        *args,
        **kwargs
) -> List[Future]:
    """
    Runs an action on each of the items in the sequence.

    Args:
        items: The items to perform the action on.
        action: The action to perform on each item.
        *args: Any parameters to add to the action to be performed.
        **kwargs: Any parameters to add to the action to be performed.

    Returns:
        A list of Futures containing the calls on the thread pool.
    """
    futures = []
    with ThreadPoolExecutor() as thread_pool:
        for item in items:
            future = thread_pool.submit(action, item, *args, **kwargs)
            futures.append(future)
    return futures


def difference(
        first: Iterator,
        second: Iterator) -> Iterator:
    """
    Gets the difference of the two sequences.

    Args:
        first:  A sequence whose elements are to be diffed.
        second: A sequence whose elements will be used to diff from the first sequence.

    Returns:
        A sequence containing the set difference between the elements of the two sequences.
    """
    values = set(first) - set(second)
    return list(values)


def unique_extend(
        first: Iterator,
        second: Iterator) -> Iterator:
    """
    Extends a sequence with unique elements of a second sequence

    Args:
        first: A sequence to extend with unique elements of another sequence
        second: A sequence to add unique elements to the first sequence

    Returns:
        A sequence adding only new elements to the initial sequence
    """
    unique_values = difference(second, first)
    result = first + unique_values
    return result
