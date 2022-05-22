"""
Base exception for Python errors.
"""

import os
from typing import Callable, List
import traceback
from _iterables import flatten, unwrap


class ExceptionBase(Exception):
    """
    An exception that occurs when a process has an error.
    """

    def __init__(
            self,
            message: str,
            inner_exception: Exception = None):
        """
        Initializes a new instance of the ExceptionBase class.

        Args:
            message:
                The message describing the error to an end user.
            inner_exception:
                An inner exception that may have caused this error.
                -or-
                None, when no previous error caused this error.
        """
        super().__init__(message)
        self._message = message
        self._inner_exception = inner_exception

    @property
    def message(self) -> str:
        """
        Gets the message of the error.
        """
        return self._message

    @property
    def inner_exception(self) -> Exception:
        """
        Gets the inner exception that caused this exception.
        """
        return self._inner_exception

    @property
    def traceback(self) -> str:
        """
        Gets the traceback information of this exception.
        """
        lines = traceback.format_exception(type(self), self, self.__traceback__)
        message = flatten(lines, '')
        return message

    def unwrap(self) -> List[Exception]:
        """
        Unwraps this exception and all inner exceptions into a list.

        Returns:
            A list containing this exception and all inner exceptions.
        """
        errors = unwrap(self, self._get_inner_exception)
        return errors

    def flatten(self) -> str:
        """
        Flattens this exception and all inner exceptions to a single str.

        Returns:
            This exception and all inner exceptions to a single str.
        """
        message = self._flatten(lambda error: str(error))
        return message

    def _flatten(
            self,
            formatter: Callable[[Exception], str]):
        """
        Flattens this exception and all inner exceptions to a single str
        with the specified formatter.

        Returns:
            This exception and all inner exceptions to a single str
            with the specified formatted text.
        """
        errors = self.unwrap()
        messages = [formatter(error) for error in errors]
        message = flatten(messages, os.linesep)
        return message

    @staticmethod
    def _get_inner_exception(exception) -> Exception:
        """
        Gets the inner exception, if any.

        Args:
            exception:
                The exception containing an inner exception.

        Returns:
            The inner exception
            - or -
            None
        """
        exception = exception.inner_exception if hasattr(exception, 'inner_exception') else None
        return exception
