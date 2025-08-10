# Output Marker

Differential programming in `warp` requires you place all `input` parameters ahead of `output` parameters in kernel function, and provide inputs and outputs accordingly on lauching kernel, which bring implicit constaint and add mental burden on lauching kernel.

```python
@warp.kernel
def func(read: wp.array(...), write: wp.array(...)): ...

warp.launch(func, shape, inputs = (read,), outputs = (write,))
```

In this example, you have to place `read` ahead of `write` in parameters. When defining `func`, you have no way to tell the type system `read` is `input` and `write` is `output`, which you have to figure out every time launching `func`, providing parameters in `inputs` and `outputs` correctly.

```python
from warp_hint import Out, kernel

@kernel
def func(write: Out[wp.array(...)], read: wp.array(...)): ...

func(shape, write, read)
```

Thanks to [alias resolve](./alias_resolve.md), `warp_hint` let you use a generic alias to mark a parameter is `output`, and place it anywhere in the type annotations of kernel function parameters.

```python
@kernel
def func(a: Out[int], b: int, c: Out[int], d: int, ...): ...

func(a, b, c, d, ...)

```

You can very arbitarily mark the `output` parameters, not affecting the [kernel call](./kernel_call.md).
