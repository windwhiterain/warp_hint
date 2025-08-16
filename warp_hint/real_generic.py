from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from warp_hint.common import VariableType, InvariableType, get_literal

@dataclass
class GenericInfo:
    specification_cache: dict[tuple[Any, ...], Specification]

class Generic:
    ___warp_hint_generic__: GenericInfo

    def __init_subclass__(cls) -> None:
        cls.___warp_hint_generic__ = GenericInfo({})

    def __class_getitem__(cls, args: tuple[Any, ...]) -> Specification:
        if not isinstance(args, tuple):
            args = (args,)
        args = tuple(get_literal(arg) for arg in args)
        params = cls.__type_params__
        assert len(args) == len(params), (args, params)
        param2arg = dict(zip(params, args))
        return specialize_from(cls, param2arg)  # type: ignore

    @classmethod
    def cls_attr(cls, type_var: VariableType) -> InvariableType | VariableType | None:
        if isinstance(cls, Specification):
            if ret := cls.___warp_hint_specification__.param2arg.get(type_var):
                return ret
            else:
                for base in cls.__bases__:
                    if issubclass(base, Generic):
                        if ret := base.cls_attr(type_var):
                            return ret
        return None

    @classmethod
    def __on_specialize__(cls): ...


@dataclass
class SpecificationInfo:
    origin: type[Generic]
    args: tuple[Any, ...]
    param2arg: dict[VariableType, Any]
    base: Specification


specificaion_meta_cache = dict[type, type]()


class Specification(type):
    ___warp_hint_specification__: SpecificationInfo

def get_specialize_meta(meta: type):
    if ret := specificaion_meta_cache.get(meta):
        return ret
    ret = type(f"{meta}(specification)", (meta, Specification), {})
    specificaion_meta_cache[meta] = ret
    return ret


def specialize_from(
    origin: type[Generic],
    param2arg: dict[VariableType, Any],
):
    cls = (
        Specification
        if origin.__class__ in (type, Specification)
        else get_specialize_meta(type(origin))
    )

    params = origin.__type_params__
    if isinstance(origin, Specification):
        info = origin.___warp_hint_specification__
        if info.base == origin:
            params = info.args
            origin = info.origin
    args: tuple[Any, ...] = tuple(
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
            specialized_base = specialize_from(base, param2arg)  # type: ignore
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
        f"{origin.__name__}[{','.join((i.__name__ if isinstance(i, type) else str(i)) for i in args)}]",
        tuple(bases),
        {
            "___warp_hint_specification__": info,
        },
    )
    assert issubclass(ret, Generic)
    specification_cache[args] = ret  # type: ignore
    info.base = ret  # type: ignore
    ret.__on_specialize__()
    return ret

