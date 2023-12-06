# https://adventofcode.com/2023/day/3
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import Iterator, List, NamedTuple
import re

import pytest


EXAMPLE_SCHEMATIC = dedent(
    """
    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..
    """
)


def test_part1():
    assert part1(EXAMPLE_SCHEMATIC) == 4361


def part1(text: str) -> int:
    schematic = Schematic.from_string(text)
    return sum(schematic.part_numbers())


def test_parse_schematic():
    g = Schematic.from_string(EXAMPLE_SCHEMATIC)
    assert g.height == 10
    assert g.width == 10
    assert g.at(0, 0) == "4"
    assert g.at(6, 3) == "#"


def test_extract_numbers():
    g = Schematic.from_string(EXAMPLE_SCHEMATIC)
    numbers = list(g.numbers())
    assert numbers == [
        (467, 0, 2, 0),
        (114, 5, 7, 0),
        (35, 2, 3, 2),
        (633, 6, 8, 2),
        (617, 0, 2, 4),
        (58, 7, 8, 5),
        (592, 2, 4, 6),
        (755, 6, 8, 7),
        (664, 1, 3, 9),
        (598, 5, 7, 9),
    ]


@dataclass
class Schematic:
    lines: List[str]

    @classmethod
    def from_string(cls, text: str) -> Schematic:
        return cls(lines=[line for line in text.splitlines() if line])

    @property
    def height(self):
        return len(self.lines)

    @property
    def width(self):
        return len(self.lines[0])

    def at(self, x: int, y: int) -> str:
        return self.lines[y][x]

    def numbers(self) -> Iterator[Number]:
        for y in range(self.height):
            x_start = x_end = None
            number = ""
            for x in range(self.width):
                char = self.at(x, y)
                if char.isdigit():
                    if x_start is None:
                        x_start = x
                    x_end = x
                    number += char
                else:
                    if x_start is not None:
                        yield Number(int(number), x_start, x_end, y)
                        x_start = x_end = None
                        number = ""
            if x_start is not None:
                yield Number(int(number), x_start, x_end, y)

    def surrounding_symbols(self, number: Number) -> Iterator[Symbol]:
        for y_ in range(number.y - 1, number.y + 2):
            for x_ in range(number.x_start - 1, number.x_end + 2):
                if (0 <= x_ < self.width) and (0 <= y_ < self.height):
                    char = self.at(x_, y_)
                    if not re.match(r"\d|\.", char):
                        yield Symbol(char, x_, y_)

    def part_numbers(self) -> List[int]:
        number_to_symbols = defaultdict(set)
        for number in self.numbers():
            for symbol in self.surrounding_symbols(number):
                number_to_symbols[number].add(symbol)
        return [number.value for number in number_to_symbols]


class Number(NamedTuple):
    value: int
    x_start: int
    x_end: int
    y: int


class Symbol(NamedTuple):
    char: str
    x: int
    y: int


if __name__ == "__main__":
    puzzle_input = Path("day03.txt").read_text()
    print("Part 1", part1(puzzle_input))
