from __future__ import annotations
from collections.abc import Iterable, Sequence
from types import new_class
from typing import Any, Self, dataclass_transform, get_type_hints, overload
import warp
import numpy
import warp.codegen
from warp_hint.alias import VariableType, resolve
from warp_hint.common import ElementType, ElementTypeBase, InvariableType
from warp_hint.real_generic import Generic, Specification
from typing import Literal as L


class WrapperType:
    __inner__: Any = None
    __inner_instance__: Any


def get_inner(x: Any) -> Any:
    if not isinstance(x, type):
        return x
    if issubclass(x, WrapperType):
        return x.__inner__
    return x


def get_inner_instance(x: Any) -> Any:
    if isinstance(x, WrapperType):
        return x.__inner_instance__
    return x


class GenericWrapperType(WrapperType, Generic):
    @classmethod
    def __gen_inner__(cls) -> Any:
        raise NotImplementedError()

    @classmethod
    def __on_specialize__(cls):
        cls.__inner__ = cls.__gen_inner__()


class Array[dtype, ndim: int](GenericWrapperType):
    @classmethod
    def __gen_inner__(cls) -> Any:
        return warp.array(dtype=get_inner(cls.cls_attr(dtype)), ndim=cls.cls_attr(ndim))  # type: ignore

    @classmethod
    def zero(cls, shape) -> Self:
        return warp.zeros(shape, dtype=get_inner(cls.cls_attr(dtype)))  # type: ignore

    @classmethod
    def empty(cls, shape) -> Self:
        return warp.empty(shape, dtype=get_inner(cls.cls_attr(dtype)))  # type: ignore

    @overload
    @classmethod
    def from_py[dtype_: ElementType](
        cls, data: Iterable[dtype_]
    ) -> Array[dtype_, L[1]]: ...

    @overload
    @classmethod
    def from_py[dtype_: ElementType](
        cls, data: Iterable[Iterable[dtype_]]
    ) -> Array[dtype_, L[2]]: ...

    @overload
    @classmethod
    def from_py[dtype_: ElementType](
        cls, data: Iterable[Iterable[Iterable[dtype_]]]
    ) -> Array[dtype_, L[3]]: ...

    @overload
    @classmethod
    def from_py[dtype_: ElementType](
        cls, data: Iterable[Iterable[Iterable[Iterable[dtype_]]]]
    ) -> Array[dtype_, L[4]]: ...

    @classmethod
    def from_py(cls, data):
        dtype_ = None

        def convert(x):
            nonlocal dtype_
            if isinstance(x, Iterable):
                return [convert(i) for i in x]
            else:
                dtype_ = get_inner(type(x))
                return get_inner_instance(x)

        data = convert(data)
        return warp.array(data, dtype=dtype_)  # type: ignore

    @classmethod
    def from_numpy[dtype_](
        cls, data: numpy.typing.NDArray[dtype_]
    ) -> Array[dtype_, Any]:
        return warp.from_numpy(data)  # type: ignore

    def numpy(self) -> numpy.typing.NDArray[dtype]:
        return self.numpy()  # type: ignore

    def __getitem__(self, idx) -> dtype: ...
    def __setitem__(self, idx, value: dtype) -> None: ...


class GenericStruct(GenericWrapperType, ElementTypeBase):
    @classmethod
    def __gen_inner__(cls) -> Any:
        annotations = cls.__annotations__
        annotations = warp.codegen.eval_annotations(annotations, cls)
        assert isinstance(annotations, dict)
        for name, annotation in annotations.items():
            annotation = resolve(annotation, resolve_arg=cls.cls_attr)
            assert isinstance(annotation, InvariableType)
            annotation = get_inner(annotation)
            annotations[name] = annotation
        cls_temp = type(f"{cls.__name__}".replace("[", "_").replace("]", "_"), (), {})
        cls_temp.__annotations__ = annotations
        return warp.struct(cls_temp)  # type: ignore

    def __getattr__(self, name: str) -> Any:
        return getattr(self.__inner_instance__, name)

    def __setattr__(self, name: str, value: Any) -> None:
        setattr(self.__inner_instance__, name, value)

    def __init__(self) -> None:
        super().__init__()
        self.__dict__["__inner_instance__"] = self.__inner__()
