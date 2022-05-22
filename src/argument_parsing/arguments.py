from .property_argument_parser import PropertyArgumentParser
from .argument import Argument
from ._inspection import get_initialization_args, get_fields
from argparse import HelpFormatter, ArgumentDefaultsHelpFormatter
from typing import ClassVar, Dict, List, Type, TypeVar
import inspect


TArgument = TypeVar('TArgument', bound='Arguments', covariant=True)


class Arguments:

    _default_formatter = ArgumentDefaultsHelpFormatter

    def __init__(
            self,
            *args,
            **kwargs
            ) -> None:
        pass

    @classmethod
    def parse(
            cls: ClassVar[TArgument]
            ) -> TArgument:
        """
        Parses the script arguments.

        Returns:
            The parsed arguments from the script.
        """
        parsed_args = cls._parse_arguments()
        instance = cls._create_instance(parsed_args)
        return instance

    @classmethod
    def get_help(
            cls: ClassVar[TArgument],
            formatter: Type[HelpFormatter] = _default_formatter
            ) -> str:
        parser = PropertyArgumentParser(formatter_class=formatter)
        property_args = cls._get_arguments_without_class_reference()
        cls._add_arguments(parser, property_args)
        help_text = parser.format_help()
        return help_text

    @classmethod
    def _create_instance(
            cls: ClassVar[TArgument],
            parsed_args: List[Argument]
            ) -> TArgument:
        initialization_params = cls._get_initialization_params(parsed_args)
        instance = cls(**initialization_params)
        cls._set_optional_args(instance, parsed_args)
        return instance

    @classmethod
    def _get_initialization_params(
            cls: ClassVar[TArgument],
            parsed_args: List[Argument]
            ) -> Dict[str, str]:
        initialization_args = [arg for arg in parsed_args if cls._use_initializer(arg)]
        initialization_params = {arg.name: arg.value for arg in initialization_args}
        return initialization_params

    @classmethod
    def _use_initializer(
            cls: ClassVar[TArgument],
            arg: Argument
            ) -> bool:
        use_initializer = arg.has_initializer and (arg.fset is not None or arg.required)
        return use_initializer

    @classmethod
    def _set_optional_args(
            cls: ClassVar[TArgument],
            instance: TArgument,
            parsed_args: List[Argument]
            ) -> None:
        optional_args = [arg for arg in parsed_args if arg.fset]
        for optional_arg in optional_args:
            instance.__setattr__(optional_arg.name, optional_arg.value)

    @classmethod
    def _parse_arguments(
            cls: ClassVar[TArgument]
            ) -> List[Argument]:
        """
        Parses the arguments from the script arguments.
        """
        parser = PropertyArgumentParser()
        args = cls._get_arguments_without_class_reference()
        cls._parse_and_check_args(args, parser)
        return args

    @classmethod
    def _parse_and_check_args(
            cls: ClassVar[TArgument],
            args: List[Argument],
            parser: PropertyArgumentParser
            ):
        cls._check_required_args(args)
        cls._add_arguments(parser, args)
        parsed_args = cls._parse_known_args(parser)
        cls._assign_parsed_values(args, parsed_args)

    @classmethod
    def _check_required_args(
            cls: ClassVar[TArgument],
            args: List[Argument]
            ) -> None:
        required_params = cls._get_required_initialization_params()
        cls._mark_required_args(args, required_params)

    @classmethod
    def _parse_known_args(
            cls: ClassVar[TArgument],
            parser: PropertyArgumentParser
            ) -> Dict[str, str]:
        namespace, _ = parser.parse_known_args()
        args = get_fields(namespace)
        return args

    @classmethod
    def _get_required_initialization_params(
            cls: ClassVar[TArgument]
            ) -> List[inspect.Parameter]:
        init_args = get_initialization_args(cls)
        required_args = [arg for arg in init_args if cls._has_required_initializer(arg)]
        return required_args

    @classmethod
    def _assign_parsed_values(
            cls: ClassVar[TArgument],
            property_args: List[Argument],
            args: Dict[str, str]
            ) -> None:
        for property_arg in property_args:
            for name, value in args.items():
                if property_arg.name == name:
                    property_arg.value = value

    @classmethod
    def _mark_required_args(
            cls: ClassVar[TArgument],
            args: List[Argument],
            params: List[inspect.Parameter]
            ) -> None:
        for arg in args:
            for param in params:
                if arg.name == param.name:
                    cls._set_required_arg(arg, param)

    @classmethod
    def _set_required_arg(
            cls: ClassVar[TArgument],
            arg: Argument,
            param: inspect.Parameter
            ) -> None:
        arg.has_initializer = True
        arg.required = cls._has_required_initializer(param) and arg.default is None
        cls._assert_argument_can_be_set(arg)

    @staticmethod
    def _has_required_initializer(
            param: inspect.Parameter
            ) -> bool:
        is_required = param.default is inspect.Parameter.empty
        return is_required

    @staticmethod
    def _assert_argument_can_be_set(
            arg: Argument
            ) -> None:
        can_be_set = arg.fset or arg.required
        if not can_be_set:
            error = (f'{arg.name} Argument must have a setter or '
                     f'a non-default initialization arg defined in its __init__ method.')
            raise AttributeError(error)

    @classmethod
    def _add_arguments(
            cls: ClassVar[TArgument],
            parser: PropertyArgumentParser,
            property_args: List[Argument]
            ) -> None:
        """
        Adds all the public fields of the class to the argument parser.
        """
        for property_arg in property_args:
            parser.add_argument_details(property_arg)

    @classmethod
    def _get_arguments_without_class_reference(
            cls: ClassVar[TArgument]
            ) -> List[Argument]:
        members = inspect.getmembers(cls, cls._is_arg)
        args = [member[1] for member in members]
        return args

    @staticmethod
    def _is_arg(
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
        property_instance = isinstance(item, Argument)
        return property_instance
