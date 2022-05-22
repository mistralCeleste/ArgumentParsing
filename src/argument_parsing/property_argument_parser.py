import argparse
from .argument import Argument
from .argument_parse_error import ArgumentParseError


class PropertyArgumentParser(argparse.ArgumentParser):

    _flag = '--'

    def error(
            self,
            message: str
            ) -> None:
        """
        Prints a usage message incorporating the message to stderr and exits.

        Raises:
            ArgumentParseError: An error with parsing the arguments occurred.
        """
        self.print_usage()
        raise ArgumentParseError(message)

    def add_argument_details(
            self,
            arg: Argument
            ) -> None:
        arg_name = self._flag + arg.name
        self.add_argument(
            arg_name,
            action=arg.action,
            default=arg.default,
            type=arg.type,
            metavar=arg.metavar,
            required=arg.required,
            help=arg.help)
