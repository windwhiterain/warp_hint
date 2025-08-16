from types import GenericAlias
from typing import Literal as L, ParamSpec, TypeVarTuple, get_args, get_origin
from typing import TypeAliasType, TypeVar

VariableType = TypeVar | ParamSpec | TypeVarTuple
InvariableType = type

ResolvedType = InvariableType | VariableType
Alias = TypeAliasType | GenericAlias


def get_literal(literal_or_value):
    if origin := get_origin(literal_or_value):
        if origin is L:
            return get_args(literal_or_value)[0]
    return literal_or_value


class ElementTypeBase: ...

ElementType = int | float | ElementTypeBase