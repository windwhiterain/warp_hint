import warp
from warp_hint.real_generic import Generic
from warp_hint.wrapper_type import Array


@warp.kernel
def func(a: Array[int, 1].inner()):
    i = warp.tid()
    a[i] = 2


a = Array[int, 3].zero(3)

warp.launch(func, 3, (a,))
