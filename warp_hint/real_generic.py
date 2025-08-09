from __future__ import annotations
from types import MethodType
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from warp_hint.common import ResolvedAlias


class RealGeneric:
    __real_alias__: RealGenericAlias

    def __class_getitem__(cls, *args):
        return RealGenericAlias(cls, args)

    @classmethod
    def type_arg(cls, type_var: TypeVar) -> ResolvedAlias:
        return cls.param2arg[type_var]  # type: ignore


class RealGenericAlias(type):
    def __new__(cls, origin: type[RealGeneric], args: tuple[ResolvedAlias, ...]):
        return super().__new__(cls, "RealGenericAlias", (origin,), {})

    def __init__(self, origin: type[RealGeneric], args: tuple[ResolvedAlias, ...]):
        self.__origin__ = origin
        self.__args__ = args
        self.param2arg = dict(
            (param, args[i]) for i, param in enumerate(origin.__type_params__)
        )
        super().__init__("RealGenericAlias", (origin,), {})

    def __getattr__(self, name: str) -> Any:
        ret = getattr(self.__origin__, name)
        if isinstance(ret, MethodType):
            return lambda *arg, **kwargs: ret.__func__(self, *arg, **kwargs)

    def __call__(self, *args, **kwargs) -> RealGeneric:
        ret = self.__origin__(*args, **kwargs)
        ret.__class__ = self  # type: ignore
        return ret
