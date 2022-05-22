from .property_like import PropertyLike
from typing import Callable, List, Type, ClassVar


class Argument(PropertyLike):

    _default_action = 'store'
    _default_type = str

    def __init__(
            self,
            help: str = None,
            type: Type = None,
            default: any = None,
            nargs: str = None,
            const: any = None,
            choices: List[str] = None,
            metavar: str = None,
            required: bool = False,
            action: str = None
            ) -> None:
        super().__init__()
        self.help = help
        self.default = default
        self.value = default
        self.nargs = nargs
        self.const = const
        self.choices = choices
        self.required = required
        self.name = None
        self.overridden_type = type
        self.type = None
        self.metavar = metavar
        self.overridden_action = action
        self.action = None
        self.has_initializer = False

    def __call__(
            self,
            wrapped: callable
            ) -> 'Argument':
        self.getter(wrapped)
        return self

    def __get__(
            self,
            instance: PropertyLike,
            owner: any = None
            ) -> 'Argument':
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(instance)

    def __set__(
            self,
            instance: PropertyLike,
            value: any
            ) -> None:
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(instance, value)

    def __delete__(
            self,
            instance: PropertyLike
            ) -> None:
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(instance)

    def getter(
            self,
            getter: callable
            ) -> 'Argument':
        super().getter(getter)
        self.name = getter.__name__
        self.type = self._get_type(self.fget)
        self.metavar = self.metavar or self.type.__name__
        self.action = self._get_action_type(self.type)
        self.__doc__ = self._get_doc(self.fget)
        self.help = self.help or self.__doc__
        return self

    def _get_doc(
            self,
            getter: callable
            ) -> str:
        doc = getter.__doc__ or self.help
        stripped_doc = doc.strip()
        return stripped_doc

    def _get_type(
            self,
            getter: callable
            ) -> Type:
        return_type = self.overridden_type or self._get_type_from_annotation(getter)
        resolved_type = self._resolve_generic_type(return_type)
        return resolved_type

    def _get_type_from_annotation(
            self,
            getter: callable
            ) -> Type:
        key = 'return'
        has_annotated_return = key in getter.__annotations__
        return_type = getter.__annotations__[key] if has_annotated_return else self._default_type
        return return_type

    @classmethod
    def _get_action_type(
            cls,
            value: Type
            ) -> str:
        """
        Automatically determines the action type for a value.

        Returns:
            The action type.
        """
        action = cls._default_action
        if issubclass(value, bool):
            action = 'store_switch'
        if issubclass(value, list):
            action = 'store_list'
        return action

    @classmethod
    def _resolve_generic_type(
            cls,
            value: Type
            ) -> ClassVar:
        is_list = issubclass(value, List)
        resolved_type = cls._get_first_generic_type(value) if is_list else value
        return resolved_type

    @staticmethod
    def _get_first_generic_type(
            value: Type
            ) -> Type:
        generic_types = list(value.__args__)
        first_item = Argument.get_first_item(generic_types)
        return first_item

    @staticmethod
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
