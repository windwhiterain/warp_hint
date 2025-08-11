from typing import Any, Literal, Self
import warp
from warp_hint.real_generic import Generic


class WrapperType:
    __inner__: Any

    @classmethod
    def inner(cls) -> Any:
        return cls.__inner__

    @classmethod
    def __gen_inner__(cls) -> Any:
        raise NotImplementedError()

    @classmethod
    def __specialize__(cls):
        cls.__inner__ = cls.__gen_inner__()


class Array[dtype, ndim: int](WrapperType, Generic):
    @classmethod
    def __gen_inner__(cls) -> Any:
        return warp.array(dtype=cls.type_attr(dtype), ndim=cls.type_attr(ndim))  # type: ignore

    @classmethod
    def zero(cls, shape) -> Self:
        return warp.zeros(shape, dtype=cls.type_attr(dtype))

    @classmethod
    def empty(cls, shape) -> Self:
        return warp.empty(shape, dtype=cls.type_attr(dtype))
