from __future__ import annotations
from dataclasses import dataclass
from types import MethodType
from typing import Any
from warp_hint.common import VariableType, InvariableType

@dataclass
class GenericInfo:
    specification_cache: dict[tuple[InvariableType | VariableType, ...], Specification]

class Generic:
    ___warp_hint_generic__ = GenericInfo({})

    def __class_getitem__(cls, *args: InvariableType | VariableType) -> Specification:
        params = cls.__type_params__
        assert len(args) == len(params)
        param2arg = dict(zip(params, args))
        return Specification.__sepcialize__(cls, param2arg)  # type: ignore

    @classmethod
    def type_attr(cls, type_var: VariableType) -> InvariableType | VariableType | None:
        if isinstance(cls, Specification):
            if ret := cls.___warp_hint_specification__.param2arg.get(type_var):
                return ret
            else:
                for base in cls.__bases__:
                    if issubclass(base, Generic):
                        if ret := base.type_attr(type_var):
                            return ret
        return None


@dataclass
class SpecificationInfo:
    origin: type[Generic]
    args: tuple[type | VariableType, ...]
    param2arg: dict[VariableType, InvariableType | VariableType]
    base: Specification


class Specification(type):
    ___warp_hint_specification__: SpecificationInfo

    @classmethod
    def __sepcialize__(
        cls,
        origin: type[Generic],
        param2arg: dict[VariableType, InvariableType | VariableType],
    ):
        params = origin.__type_params__
        if isinstance(origin, Specification):
            info = origin.___warp_hint_specification__
            if info.base == origin:
                params = info.args
                origin = info.origin
        args: tuple[type | VariableType, ...] = tuple(
            param2arg.get(i) if isinstance(i, VariableType) else i for i in params
        )  # type: ignore
        params = origin.__type_params__

        if None in args:
            return origin

        specification_cache = origin.___warp_hint_generic__.specification_cache
        if specification := specification_cache.get(args):
            return specification

        bases: list[type] = []
        for base in origin.__bases__:
            if isinstance(base, Specification):
                assert issubclass(base, Generic)
                specialized_base = cls.__sepcialize__(base, param2arg)  # type: ignore
                if specialized_base is not base:
                    bases.append(specialized_base)
        bases.append(origin)

        info = SpecificationInfo(
            origin,  # type: ignore
            args,  # type: ignore
            dict(zip(params, args)),  # type: ignore
            None,  # type: ignore
        )
        ret = cls(
            origin.__name__ + "".join(f"[{i.__name__}]" for i in args),
            tuple(bases),
            {
                "___warp_hint_specification__": info,
            },
        )
        specification_cache[args] = ret
        info.base = ret
        return ret

    def __call__(self, *args, **kwargs) -> Generic:
        ret = self.___warp_hint_specification__.origin(*args, **kwargs)
        ret.__class__ = self  # type: ignore
        return ret
