# https://adventofcode.com/2023/day/14
from __future__ import annotations

from array import array
from textwrap import dedent
from typing import Iterator, Self, Tuple

import numpy as np

import pytest


EXAMPLE = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


def test_matrix():
    m = Matrix(EXAMPLE)
    assert m.width == 10
    assert m.height == 10
    assert (
        str(m)
        == dedent(
            """
            O....#....
            O.OO#....#
            .....##...
            OO.#O....O
            .O.....O#.
            O.#..O.#.#
            ..O..#O..O
            .......O..
            #....###..
            #OO..#....
            """
        ).strip()
    )

    assert m[1, 1] == "O"
    assert m[6, 1] == "#"
    m[6, 1] = "."
    assert m[6, 1] == "."


class Matrix:
    data: np.ndarray  # https://numpy.org/doc/stable/reference/arrays.html

    def __init__(self, text: str):
        self.data = np.array(
            [list(line) for line in text.strip().splitlines()],
            dtype=(str, 1),
        )

    def __str__(self) -> str:
        return "\n".join("".join(s for s in line) for line in self.data.tolist())

    @classmethod
    def from_string(cls, text: str) -> Self:
        return cls(text)

    @property
    def width(self):
        return self.data.shape[1]

    @property
    def height(self):
        return self.data.shape[0]

    def __getitem__(self, key: Tuple[int, int]) -> str:
        x, y = key
        return self.data[y - 1, x - 1]

    def __setitem__(self, key: Tuple[int, int], value: str) -> None:
        x, y = key
        self.data[y - 1, x - 1] = value


@pytest.fixture
def platform():
    return Platform.from_string(EXAMPLE)


def test_rounded_rocks_in_column(platform):
    assert list(platform.rounded_rocks_in_column(1)) == [1, 2, 4, 6]


def test_tilt(platform):
    platform.tilt()
    assert (
        str(platform)
        == dedent(
            """\
            OOOO.#.O..
            OO..#....#
            OO..O##..O
            O..#.OO...
            ........#.
            ..#....#.#
            ..O..#.O.O
            ..O.......
            #....###..
            #....#....
            """
        ).strip()
    )


class Platform(Matrix):
    def rounded_rocks_in_column(self, x: int) -> Iterator[int]:
        for y in range(1, self.height + 1):
            if self[x, y] == "O":
                yield y

    def tilt(self) -> None:
        for x in range(1, self.width + 1):
            for y in self.rounded_rocks_in_column(x):
                target_y = y
                while target_y > 1 and self[x, target_y - 1] == ".":
                    target_y -= 1
                self[x, y], self[x, target_y] = self[x, target_y], self[x, y]

    def total_load(self) -> int:
        return sum(
            self.height - y + 1
            for x in range(1, self.width + 1)
            for y in self.rounded_rocks_in_column(x)
        )


def test_part1():
    assert part1(EXAMPLE) == 136


def part1(text: str) -> int:
    platform = Platform.from_string(text)
    platform.tilt()
    return platform.total_load()


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
