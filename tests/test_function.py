import warp
from warp_hint.common import L
from warp_hint.function import kernel
from warp_hint.real_generic import Generic
from warp_hint.wrapper_type import Array, GenericWrapperType
from numpy.testing import assert_array_equal


def test():
    @kernel
    def func(a: Array[int, L[1]]):
        i = warp.tid()
        a[i] = i

    a = Array[int, 1].zero(3)
    func(a)(3)
    assert_array_equal(a.numpy(), Array.from_py([0, 1, 2]).numpy())


if __name__ == "__main__":
    test()
