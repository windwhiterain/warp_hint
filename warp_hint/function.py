from collections.abc import Callable
import inspect
from itertools import chain

import warp
from typing import Generic, ParamSpec

from warp_hint.alias import Effect, resolve
from warp_hint.wrapper_type import GenericWrapperType, get_inner

type Out[T] = T


class Launchable:
    def __init__(self, warp_kernel, inputs, outputs) -> None:
        self.warp_kernel = warp_kernel
        self.inputs = inputs
        self.outputs = outputs

    def __call__(self, shape) -> None:
        warp.launch(self.warp_kernel, shape, self.inputs, self.outputs)  # type: ignore


P = ParamSpec("P")


class Kernel(Generic[P]):
    def __init__(self, kernel, is_outs: list[bool]) -> None:
        super().__init__()
        self.warp_kernel = kernel
        self.is_outs = is_outs

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Launchable:
        inputs = []
        outputs = []
        for i, arg in enumerate(args):
            if not self.is_outs[i]:
                inputs.append(arg)
            else:
                outputs.append(arg)
        return Launchable(self.warp_kernel, inputs, outputs)


def kernel(func: Callable[P, None]) -> Kernel[P]:
    signature = inspect.signature(func)

    is_outs = []

    input_annotations = []
    output_annotations = []
    input_params = []
    output_params = []
    for name, param in signature.parameters.items():
        annotation = param.annotation
        is_out = False

        def out_effect(_):
            nonlocal is_out
            is_out = True

        annotation = resolve(annotation, [Effect(Out, out_effect)])
        assert isinstance(annotation, type)
        annotation = get_inner(annotation)
        is_outs.append(is_out)
        annotations = input_annotations if not is_out else output_annotations
        params = input_params if not is_out else output_params
        annotations.append((name, annotation))
        params.append(
            inspect.Parameter(
                name, inspect.Parameter.POSITIONAL_ONLY, annotation=annotation
            )
        )

    func.__annotations__ = dict(chain(input_annotations, output_annotations))
    setattr(func, "__signature__", inspect.Signature(input_params + output_params))

    kernel = warp.Kernel(func, code_transformers=[])  # type: ignore
    return Kernel(kernel, is_outs)  # type: ignore
