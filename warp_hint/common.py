from types import GenericAlias as _GenericAlias
from typing import Any, get_origin as _get_origin
from typing import get_args as _get_args
from typing import TypeAliasType, TypeVar

from warp_hint.real_generic import RealGenericAlias

GenericAlias = _GenericAlias | RealGenericAlias

Alias = TypeAliasType | GenericAlias | type | TypeVar
ResolvedAlias = type | GenericAlias


def get_origin(_: Any) -> type | None:
    if isinstance(_, RealGenericAlias):
        return _.__origin__
    else:
        return _get_origin(_)


def get_args(_: Any) -> tuple[Any, ...]:
    if isinstance(_, RealGenericAlias):
        return _.__args__
    else:
        return _get_args(_)
