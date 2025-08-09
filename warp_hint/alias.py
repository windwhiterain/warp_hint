from collections import defaultdict
from collections.abc import Callable, Iterable
from typing import TypeAliasType, TypeVar

from warp_hint.common import Alias, GenericAlias, ResolvedAlias, get_args, get_origin


class AliasEffect:
    def __init__(self, type: Alias, func: Callable[[Alias], None]) -> None:
        self.type = type
        self.func = func


def resolve_alias(alias: Alias, effects: Iterable[AliasEffect] = ()) -> ResolvedAlias:
    return ResolveAlias(effects).resolve_alias(alias, None)


class ResolveAlias:
    def __init__(self, effects: Iterable[AliasEffect]) -> None:
        self.effets = defaultdict(list)
        for effect in effects:
            self.effets[effect.type].append(effect.func)

    def resolve_alias(
        self,
        alias: Alias,
        resolve_arg: Callable[[TypeVar], ResolvedAlias | None] | None,
    ) -> ResolvedAlias:
        if effect_list := self.effets.get(alias):
            for effect in effect_list:
                effect.func(alias)
        if isinstance(alias, TypeVar):
            assert resolve_arg is not None
            ret = resolve_arg(alias)
            assert ret is not None
            return ret
        elif isinstance(alias, TypeAliasType):
            return self.resolve_alias(alias.__value__, None)
        elif isinstance(alias, GenericAlias):
            origin = get_origin(alias)
            assert origin is not None
            args = get_args(alias)
            resolved_args = map(lambda x: self.resolve_alias(x, resolve_arg), args)
            if isinstance(origin, type):
                return origin[*resolved_args]  # type: ignore
            params = origin.__type_params__
            param2arg = dict(zip(params, resolved_args))
            next = origin.__value__
            return self.resolve_alias(next, lambda x: param2arg.get(x))
        else:
            return alias
