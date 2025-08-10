from types import GenericAlias
from typing import ParamSpec, TypeVarTuple
from typing import TypeAliasType, TypeVar

VariableType = TypeVar | ParamSpec | TypeVarTuple
InvariableType = type | GenericAlias

ResolvedType = InvariableType | VariableType
Alias = TypeAliasType
