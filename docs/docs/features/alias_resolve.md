# Alias Resolve

```python
type A = int

@warp.kernel
def func(a: A): ...

```

`warp` can't infer the parameter type `A` in kernel function, `warp_hint` let you do this:

```python
type A = int

@warp_hint.kernel
def func(a: A): ...

```

Although most of the time you can use the older version of alias to make it pass in `warp`:

```python
A = int
```

However, when it comes to generic alias:

## Generic Alias Resolve

```python
A[t] = list[t]
B[t] = t
C[k,v] = dict[k,v]
D[k] = C[k,int]
E[k,v] = C[k,D[k]]

@warp_hint.kernel
def func(a: A[int], ... ,e: E[int,float]): ...
```

`warp_hint` will resolve all valid generic alias for you.

Although `warp` does not support generic type in python's type system, you can't actually use `list[t]` nor `dict[k,v]` in kernel type annotations, but `warp_hint` provide that for you.
