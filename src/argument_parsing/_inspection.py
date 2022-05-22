"""
High-level methods used for inspecting objects.
"""

import inspect
from typing import Any, ClassVar, Dict, List
from ._str_enum import StrEnum


class AccessModifier(StrEnum):
    """
    Access modifiers for names.
    """
    protected = '_'
    private = '__'
    public = ''


class ObjectFeatureTokens(StrEnum):
    """
    Tokens used to determine whether an item is an object feature.
    """
    start = '__'
    end = '__'


def is_public(
        name: str
        ) -> bool:
    """
    Determines whether the name is public.

    Args:
        name:
            The name of the item to inspect.

    Returns:
        A value indicating whether the name is public.
    """
    public = not is_private(name) and not is_protected(name)
    return public


def is_protected(
        name: str
        ) -> bool:
    """
    Determines whether the name is protected.

    Args:
        name:
            The name of the item to inspect.

    Returns:
        A value indicating whether the name is protected.
    """
    protected = name.startswith(AccessModifier.protected)
    return protected


def is_object_feature(
        name: str
        ) -> bool:
    """
    Determines whether the name is an object feature.

    Args:
        name:
            The name of the item to inspect.

    Returns:
        A value indicating whether the name is an object feature.
    """
    object_feature = name.startswith(ObjectFeatureTokens.start) \
        and name.endswith(ObjectFeatureTokens.end)
    return object_feature


def is_private(
        name: str
        ) -> bool:
    """
    Determines whether the name is private

    Remarks:
        The private naming scheme is not unique because object-features also start with the token,
        so to prevent object-features from matching a false-positive here, they are accounted for.

    Args:
        name:
            The name of the item to inspect.

    Returns:
        A value indicating whether the name is private.
    """
    private = not is_object_feature(name) and name.startswith(AccessModifier.private)
    return private


def is_property(
        item: any
        ) -> bool:
    """
    Determines whether the item is a property object.

    Args:
        item:
            The item to inspect.

    Returns:
        A value indicating whether the item is a property object.
    """
    property_instance = isinstance(item, property)
    return property_instance


def get_fields(
        item: object
        ) -> Dict[str, Any]:
    """
    Gets the fields of an object.

    Args:
        item:
            The item to get the fields of.

    Returns:
        The fields of the object.

    Raises:
        TypeError:
            The object does not implement the __dict__ attribute.
    """
    if not hasattr(item, '__dict__'):
        raise TypeError('object must implement the __dict__ attribute.')
    fields = vars(item)
    return fields


def get_public_fields(
        item: object
        ) -> Dict[str, Any]:
    """
    Gets the public fields of an object.

    Args:
        item:
            The item to get the public fields from.

    Returns:
        The public fields of the object.

    Raises:
        TypeError:
            The object does not implement the __dict__ attribute.
    """
    fields = {field: value for field, value in get_fields(item).items() if is_public(field)}
    return fields


def get_public_properties(
        item: object
        ) -> Dict[str, Any]:
    """
    Gets the public properties of the object.

    Args:
        item:
            The item to get the public properties from.

    Returns:
        The public properties of the object.
    """
    properties = inspect.getmembers(type(item), is_property)
    members = {name: getattr(item, name) for name, _ in properties if is_public(name)}
    return members


def get_callable_parameters(
        func: callable
        ) -> List[inspect.Parameter]:
    """
    Gets the parameter signature of the specified function.

    Args:
        func:
            Function to get the parameter signature of.

    Returns:
        The parameter signature of the specified function.
    """
    initialization_arguments = inspect.signature(func, follow_wrapped=True)
    parameters = [arg for _, arg in initialization_arguments.parameters.items()]
    return parameters


def get_parameters_without_class_reference(
        func: callable
        ) -> List[inspect.Parameter]:
    """
    Gets the parameter signature without the class reference of the specified function.

    Remarks:
        The class reference in the parameter signature is the first parameter,
        typically named: cls, or self.

    Args:
        func:
            Function to get the parameter signature of.

    Returns:
        The parameter signature without the class reference of the specified function.
    """
    parameters = get_callable_parameters(func)
    parameters_without_class_reference = parameters[1:]
    return parameters_without_class_reference


def get_initialization_args(
        class_var: ClassVar
        ) -> List[inspect.Parameter]:
    """
    Gets the assignable parameters of the initializer of the specified class.

    Args:
        class_var:
            Class to get the parameters of the initializer.

    Returns:
        The assignable parameters of the initializer.
    """
    parameters = get_parameters_without_class_reference(class_var.__init__)
    return parameters
