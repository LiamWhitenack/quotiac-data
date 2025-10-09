import inspect
import json
import types
import typing
from typing import get_args, get_origin

from codiac_sandbox.puzzle_types import CryptographBase
from codiac_sandbox.utils.puzzle_classes import PUZZLE_CLASSES


def save_puzzle(cls: type[CryptographBase], kwargs: dict[str, str | list[str]]) -> None:
    with open("resources/master-puzzle-list.json") as f:
        obj = cls(**kwargs)  # type: ignore[arg-type]
        add_to = json.load(f)
    with open("resources/master-puzzle-list.json", "w") as f:
        json.dump(add_to + [obj.to_json()], f, indent=2)


def get_puzzle_parameters(puzzle_type: str) -> dict[str, inspect.Parameter]:
    cls = PUZZLE_CLASSES[puzzle_type]
    sig: dict[str, inspect.Parameter] = dict(inspect.signature(cls.__init__).parameters)  # type: ignore
    for param_name, param in sig.copy().items():
        if param_name in {
            "self",
            "string_to_encrypt",
            "puzzle_type",
            "hints",
            "encryptionMap",
        } or annotation_allows_none(param):
            del sig[param_name]

    return sig


def annotation_allows_none(param: inspect.Parameter) -> bool:
    annotation = param.annotation

    # If annotation is not set
    if annotation is inspect.Parameter.empty:
        return False

    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin is types.UnionType or origin is typing.Union:  # type: ignore
        return type(None) in args

    return False
