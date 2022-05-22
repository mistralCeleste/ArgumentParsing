"""
A module used to extend enums.
"""

import enum
from ._iterables import flatten


class StrEnum(str, enum.Enum):
    """
    Enum where members are also (and must be) str
    """

    @classmethod
    def has_member(
            cls,
            member: str):
        included = member in cls.__members__
        return included

    @classmethod
    def assert_member_is_defined(
            cls,
            member: str):
        if not cls.has_member(member):
            error_pattern = ('The member \'{member}\' is not a valid value for \'{type}\', '
                             'expected members are: \'{members}\'')
            members = flatten(cls.__members__.keys(), ', ')
            error = error_pattern.format(
                member=member,
                type=cls.__name__,
                members=members)
            raise KeyError(error)

    @classmethod
    def from_name(
            cls,
            name: str):
        """
        Gets the enum item from the name of the item.

        Remarks:
            Normally an Enum(value) is for the value of the item, but from_name(name) will get the
            enum item from the name (instead of the from the value.)

        Args:
            name:
                The name of the enum to get.

        Raises:
            KeyError:
                The name was not found in the enum.

        Returns:
            The enum item from the specified name.
        """
        cls.assert_member_is_defined(name)
        item = cls[name]
        return item

    def __str__(self):
        """
        Gets the text value of the enum.
        """
        return self.value

    def __repr__(self):
        """
        Gets the text value of the enum.
        """
        return self.value
