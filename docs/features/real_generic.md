# Real Generic

Python' generic is kind a fake generic that there is no specialization but generic alias.

```python
class A[T]:
    @staticmethod
    def cls_info(self):
        print(T)

    def info(self):
        print(T)

A[int].info() # T
A[int]().info() # T
print(issubclass(A[int],A)) # False
print(isinstance(A[int](),A[int])) # False
print(isinstance(A[int](),A)) # True
```

In this example, you can't get the resolved value of the type var `T` in any kind of method of class. Type alias `A[int]` is not subclass of its origin `A`, and call type alias `A[int]` only got a instance of the origin type`A`.

```python
from warp_hint import RealGeneric

class A[T](RealGeneric):
    @staticmethod
    def cls_info(cls):
        print(cls.type_arg(T))

    def info(self):
        print(self.type_arg(T))

A[int].info() # int
A[int]().info() # int
print(issubclass(A[int],A)) # True
print(isinstance(A[int](),A[int])) # True
print(isinstance(A[int](),A)) # True
```

`warp_hint` enable all of this, resolved type variable value can be retrieved via a class method `type_arg`, type alias `A[int]` become a real specification that subclass `A`.
