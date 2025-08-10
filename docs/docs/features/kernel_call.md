# Kernel Call

In `warp`, launching a kernel is tedious and lost all type-hint of the kernel function:

```python
@warp.kernel
def func(a: int, b: float): ...

warp.launch(func, shape, inputs = (1, 1.0))
```

`warp_hint` enable you directly call the kernel function with `shape` added ahead of parameter annotations:

```python
from warp_hint import kernel 

@kernel
def func(a: int, b: float): ...

func(shape, 1, 1.0) # type-hint is avaliable
```
