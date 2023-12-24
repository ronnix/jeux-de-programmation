from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import Any, NamedTuple, Self


class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (+1, 0)
    UP = (0, -1)
    DOWN = (0, +1)


class Coords(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Any) -> Coords:
        if isinstance(other, Direction):
            dx, dy = other.value
            return Coords(x=self.x + dx, y=self.y + dy)
        return NotImplemented


@dataclass(frozen=True)
class Grid:
    lines: list[str]

    @classmethod
    def from_string(cls, text: str) -> Self:
        return cls(lines=text.strip().splitlines())

    @cached_property
    def width(self) -> int:
        return len(self.lines[0])

    @cached_property
    def height(self) -> int:
        return len(self.lines)

    def at(self, x: int, y: int) -> str:
        return self.lines[y][x]

    def __str__(self):
        return "\n".join(self.lines)
