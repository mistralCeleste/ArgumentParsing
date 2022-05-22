from .exceptions import ExceptionBase


class ArgumentParseError(ExceptionBase):

    def __init__(
            self,
            message: str,
            inner_exception: Exception = None
            ) -> None:
        error = f'Argument error: {message}'
        super().__init__(error, inner_exception)
