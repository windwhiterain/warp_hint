from warp_hint.real_generic import Generic


class A[a](Generic):
    @classmethod
    def cls_get_a(cls):
        return cls.type_attr(a)

    def get_a(self):
        return self.type_attr(a)


class B[b](A[b]):
    @classmethod
    def cls_get_b(cls):
        return cls.type_attr(b)

    def get_b(self):
        return self.type_attr(b)


class C(B[int]): ...


def test_type_attr():
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

    assert B[int] is B[int]
