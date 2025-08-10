from collections.abc import Callable
import inspect
from itertools import chain

import warp
from typing import (
    ParamSpec,
    Protocol,
)

from warp_hint.alias import Effect, resolve


P = ParamSpec("P")

type Out[T] = T


class KernelImpl:
    def __init__(self, kernel, is_outs: list[bool]) -> None:
        super().__init__()
        self.kernel = kernel
        self.is_outs = is_outs

    def __call__(self, dim, *args) -> None:
        inputs = []
        outputs = []
        for i, arg in enumerate(args):
            if not self.is_outs[i]:
                inputs.append(arg)
            else:
                outputs.append(arg)
        warp.launch(self.kernel, dim, inputs, outputs)  # type: ignore


class Kernel(Protocol[P]):
    def __call__(self, dim, *args: P.args, **kwargs: P.kwargs) -> None: ...


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
    return KernelImpl(kernel, is_outs)  # type: ignore
