from collections import defaultdict
from collections.abc import Callable, Iterable
from typing import TypeAliasType, TypeVar, get_args, get_origin

from warp_hint.common import Alias, GenericAlias, ResolvedType, VariableType
from warp_hint.real_generic import Generic, Specification, specialize_from


class Effect:
    def __init__(
        self, type: Alias, func: Callable[[Alias | ResolvedType], None]
    ) -> None:
        self.type = type
        self.func = func


def resolve(
    alias: Alias | ResolvedType,
    effects: Iterable[Effect] = (),
    resolve_arg: Callable[[VariableType], ResolvedType | None] | None = None,
) -> ResolvedType:
    return ResolveAlias(effects).resolve_alias(alias, resolve_arg)


class ResolveAlias:
    def __init__(self, effects: Iterable[Effect]) -> None:
        self.effects = defaultdict[Alias | ResolvedType, list[Effect]](list)
        for effect in effects:
            self.effects[effect.type].append(effect)

    def resolve_alias(
        self,
        alias: Alias | ResolvedType,
        resolve_arg: Callable[[VariableType], ResolvedType | None] | None,
    ) -> ResolvedType:
        if effect_list := self.effects.get(alias):
            for effect in effect_list:
                effect.func(alias)
        if isinstance(alias, VariableType):
            assert resolve_arg is not None
            ret = resolve_arg(alias)
            assert ret is not None
            return ret
        elif isinstance(alias, TypeAliasType):
            return self.resolve_alias(alias.__value__, None)
        elif isinstance(alias, GenericAlias):
            origin = get_origin(alias)
            if isinstance(origin, type):
                return origin
            args = get_args(alias)
            resolved_args = map(lambda x: self.resolve_alias(x, resolve_arg), args)
            params = origin.__type_params__
            param2arg = dict(zip(params, resolved_args))
            next = origin.__value__
            return self.resolve_alias(next, lambda x: param2arg.get(x))
        elif isinstance(alias, Specification):
            info = alias.___warp_hint_specification__
            args = info.args
            resolved_args = map(lambda x: self.resolve_alias(x, resolve_arg), args)
            param2arg = dict(zip(args, resolved_args))
            return specialize_from(alias, param2arg)  # type: ignore
        else:
            return alias
