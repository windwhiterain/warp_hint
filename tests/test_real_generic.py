from warp_hint.real_generic import Generic


class A[a](Generic):
    def __init__(self) -> None:
        self._a = self.cls_attr(a)

    @classmethod
    def cls_get_a(cls):
        return cls.cls_attr(a)

    def get_a(self):
        return self.cls_attr(a)


class B[b](A[b]):
    def __init__(self) -> None:
        super().__init__()
        self._b = self.cls_attr(b)
    @classmethod
    def cls_get_b(cls):
        return cls.cls_attr(b)

    def get_b(self):
        return self.cls_attr(b)


class C(B[int]): ...


def test_cls_attr():
    assert A[int].cls_get_a() is int
    assert A[int]().cls_get_a() is int
    assert A[int]().get_a() is int

    assert B[int].cls_get_b() is int
    assert B[int]().cls_get_b() is int
    assert B[int]().get_b() is int

    assert B[int].cls_get_a() is int
    assert B[int]().cls_get_a() is int
    assert B[int]().get_a() is int

    assert C.cls_get_a() is int
    assert C().cls_get_a() is int
    assert C().get_a() is int

    assert C.cls_get_b() is int
    assert C().cls_get_b() is int
    assert C().get_b() is int

    assert A[int]()._a is int
    assert B[int]()._a is int
    assert B[int]()._b is int


def test_inheritance():
    assert B[int] is B[int]
    assert issubclass(A[int], A)
    assert issubclass(B[int], A[int])  # type: ignore
    assert issubclass(B, A)
    assert not issubclass(B, A[int])  # type: ignore
    assert not issubclass(B[float], A[int])  # type: ignore
    assert issubclass(C, B)
    assert issubclass(C, B[int])  # type: ignore
    assert not issubclass(C, A[float])  # type: ignore


if __name__ == "__main__":
    test_cls_attr()
    test_inheritance()