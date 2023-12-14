from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import NamedTuple, Self


class Coords(NamedTuple):
    x: int
    y: int


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
