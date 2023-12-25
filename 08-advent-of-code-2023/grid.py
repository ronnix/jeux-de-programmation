from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import Any, NamedTuple, Self


class Coords(NamedTuple):
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other: Any) -> Coords:
        if isinstance(other, Coords):
            return Coords(x=self.x + other.x, y=self.y + other.y)
        if isinstance(other, Direction):
            return self + other.value
        return NotImplemented

    def __mul__(self, other: Any) -> Coords:
        if isinstance(other, int):
            return Coords(x=self.x * other, y=self.y * other)
        return NotImplemented


class Direction(Enum):
    LEFT = Coords(-1, 0)
    RIGHT = Coords(+1, 0)
    UP = Coords(0, -1)
    DOWN = Coords(0, +1)


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


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
