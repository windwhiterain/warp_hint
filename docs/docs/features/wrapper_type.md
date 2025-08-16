# Wrapper Type

Thanks to [real generic](./real_generic.md), `warp_hint` can wrap type created with type parameters into python generic, enbaling type-hint.

```python
from warp_hint.wrapper_type import Array

type ArrayInt1D = Array[A[int], 1]
print(Array[A[int], 1].zero(3))

a = Array.from_py([1, 1, 1]) # type-hint is avaliable
```

In this example, `warp_hint` provide a builtin wrapper type `Array` to wrap `warp.array`.

## Generic Wrapper Struct

You can't decorate generic class with `@struct` in `warp`, but you can in `warp_hint`.

```python
from warp_hint.wrapper_type import GenericWrapperStruct

class Point[T](GenericStruct):
    x: T
    y: T

p = Point[float]()
p.x = 1.0
p.y = 2.0
print(p)
```

Arbitary nesting:

```python
class Segment[T]:
    start: Point[T]
    end: Point[T]
```
