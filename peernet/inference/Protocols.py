"""Inference protocol to simplify static type checking throughout the package.

The inference protocol defined here is used for dynamic runtime checking in one
place-- in enginize.py, when returning an engine from user-produced inference
object.
"""

from typing import Protocol, Any, runtime_checkable


@runtime_checkable
class Inference(Protocol):
    """Protocol for inference objects.

    Inference objects MUST have an infer() method. They may optionally
    have preprocess and postprocess methods. Preprocess and Postprocess
    are not included in the Protocol definition as they are optional.
    """

    def infer(self, *args, **kwargs) -> Any: ...  # noqa: D102
