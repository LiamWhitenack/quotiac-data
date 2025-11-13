from typing import Any, TypeVar

from quotiac_sandbox.puzzle_types import CryptographBase


def get_all_subclasses(cls: type[CryptographBase]) -> set[type[CryptographBase]]:
    subclasses = set()
    work = [cls]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses  # type: ignore[return-value]


PUZZLE_CLASSES: dict[str, type[CryptographBase]] = dict(
    sorted(
        (subclass.__name__, subclass)
        for subclass in get_all_subclasses(CryptographBase)  # type: ignore[type-abstract]
    )
)

T = TypeVar("T", bound=CryptographBase)


def from_json(cls: type[T], data: dict[str, Any]) -> T:
    return cls.from_json(data)


def parse_puzzle(data: dict[str, Any]) -> CryptographBase:
    cls = PUZZLE_CLASSES[data["type"]]
    return cls.from_json(data)
