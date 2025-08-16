import warp
from warp_hint import kernel
from warp_hint.common import L
from warp_hint.wrapper_type import Array, GenericStruct
from numpy.testing import assert_array_equal


def test():
    class A[T](GenericStruct):
        a: float
        b: T

    @kernel
    def func(a: Array[A[int], L[1]]):
        i = warp.tid()
        a[i].b = i

    a = Array[A[int], 1].zero(3)
    func(a)(3)
    a0 = A[int]()
    a0.a = 0
    a0.b = 0
    a1 = A[int]()
    a1.a = 0
    a1.b = 1
    a2 = A[int]()
    a2.a = 0
    a2.b = 2
    assert_array_equal(a.numpy(), Array.from_py([a0, a1, a2]).numpy())


if __name__ == "__main__":
    test()
