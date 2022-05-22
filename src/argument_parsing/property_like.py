class PropertyLike:

    def __init__(
            self,
            getter: callable = None,
            setter: callable = None,
            deletor: callable = None,
            doc: str = None
            ) -> None:
        self.fget = getter
        self.fset = setter
        self.fdel = deletor
        self.__doc__ = doc

    def getter(
            self,
            getter: callable
            ) -> 'PropertyLike':
        self.fget = getter
        return self

    def setter(
            self,
            setter: callable
            ) -> 'PropertyLike':
        self.fset = setter
        return self

    def deleter(
            self,
            deleter: callable
            ) -> 'PropertyLike':
        self.fdel = deleter
        return self
