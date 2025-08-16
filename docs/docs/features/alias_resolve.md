# Alias Resolve
`warp` can't infer type alias in parameter annotations in kernel function.
```python
type A = int

@warp.kernel
def func(a: A): ...

```

In this example, `A` is a type alias of `int`, but use it to annote parameter `a` in kernel function `func` is invalid. However `warp_hint` let you do this:

```python
from warp_hint import kernel 

type A = int

@kernel
def func(a: A): ...
```

Although most of the time you can use the older version of alias in `warp`:

```python
A = int
```

But when it comes to generic alias:

## Generic Alias Resolve

```python
A[t] = list[t]
B[t] = t
C[k,v] = dict[k,v]
D[k] = C[k,int]
E[k,v] = C[k,D[k]]

@kernel
def func(a: A[int], ... ,e: E[int,float]): ...
```

`warp_hint` will resolve all valid generic alias for you.

`warp` does not support generic type in python's type system, so you can't actually use `list[t]` nor `dict[k,v]` in kernel type annotations. However, `warp_hint` let you use [generic wrapper type](./wrapper_type.md).
