from typing import Union, TYPE_CHECKING, Tuple

from slither.core.solidity_types import ElementaryType
from slither.core.solidity_types.type import Type

if TYPE_CHECKING:
    from slither.core.declarations.contract import Contract
    from slither.core.declarations.enum_top_level import EnumTopLevel


# Use to model the Type(X) function, which returns an undefined type
# https://solidity.readthedocs.io/en/latest/units-and-global-variables.html#type-information
class TypeInformation(Type):
    def __init__(self, c: Union[ElementaryType, "Contract", "EnumTopLevel"]) -> None:
        # pylint: disable=import-outside-toplevel
        from slither.core.declarations.contract import Contract
        from slither.core.declarations.enum import Enum

        assert isinstance(c, (Contract, ElementaryType, Enum))
        super().__init__()
        self._type = c

    @property
    def type(self) -> "Contract":
        return self._type

    @property
    def storage_size(self) -> Tuple[int, bool]:
        """
        32 is incorrect, as Type(x) return a kind of structure that can contain
        an arbitrary number of value
        As Type(x) cannot be directly stored, we are assuming that the correct storage size
        will be handled by the fields access

        :return:
        """
        return 32, True

    @property
    def is_dynamic(self) -> bool:
        raise NotImplementedError

    def __str__(self):
        return f"type({self.type.name})"

    def __eq__(self, other):
        if not isinstance(other, TypeInformation):
            return False
        return self.type == other.type
