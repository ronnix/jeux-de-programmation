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
    m = Matrix.from_string(EXAMPLE)
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

    def __init__(self, data: np.ndarray):
        self.data = data

    def __str__(self) -> str:
        return "\n".join("".join(s for s in line) for line in self.data.tolist())

    def copy(self) -> Self:
        return self.__class__(data=self.data.copy())

    @classmethod
    def from_string(cls, text: str) -> Self:
        return cls(
            data=np.array(
                [list(line) for line in text.strip().splitlines()],
                dtype=(str, 1),
            )
        )

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


def test_tilt_north(platform):
    platform.tilt_north()
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

    def rounded_rocks_in_row(self, y: int) -> Iterator[int]:
        for x in range(1, self.width + 1):
            if self[x, y] == "O":
                yield x

    def spin_cycle(self) -> None:
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def tilt_north(self) -> None:
        self.tilt_vertically(delta=-1)

    def tilt_south(self) -> None:
        self.tilt_vertically(delta=+1)

    def tilt_vertically(self, delta: int) -> None:
        for x in range(1, self.width + 1):
            for y in sorted(self.rounded_rocks_in_column(x), reverse=delta > 0):
                target_y = y
                while (
                    1 <= target_y + delta <= self.height
                    and self[x, target_y + delta] == "."
                ):
                    target_y += delta
                self[x, y], self[x, target_y] = self[x, target_y], self[x, y]

    def tilt_west(self) -> None:
        self.tilt_horizontally(delta=-1)

    def tilt_east(self) -> None:
        self.tilt_horizontally(delta=+1)

    def tilt_horizontally(self, delta: int) -> None:
        for y in range(1, self.height + 1):
            for x in sorted(self.rounded_rocks_in_row(y), reverse=delta > 0):
                target_x = x
                while (
                    1 <= target_x + delta <= self.width
                    and self[target_x + delta, y] == "."
                ):
                    target_x += delta
                self[x, y], self[target_x, y] = self[target_x, y], self[x, y]

    def spin_cycles_periodicity(self) -> Tuple[int, int]:
        seen = {}
        cycles = 0
        platform = self.copy()
        while platform.data.tobytes() not in seen:
            if cycles > 0:
                seen[platform.data.tobytes()] = cycles
            platform.spin_cycle()
            cycles += 1
        previous = seen[platform.data.tobytes()]
        return previous, cycles - previous

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
    platform.tilt_north()
    return platform.total_load()


def test_spin_cycle(platform):
    platform.spin_cycle()
    assert (
        str(platform)
        == dedent(
            """\
            .....#....
            ....#...O#
            ...OO##...
            .OO#......
            .....OOO#.
            .O#...O#.#
            ....O#....
            ......OOOO
            #...O###..
            #..OO#....
            """
        ).strip()
    )


def test_find_cycles(platform):
    assert platform.spin_cycles_periodicity() == (3, 7)


def test_part2():
    assert part2(EXAMPLE) == 64


def part2(text: str) -> int:
    platform = Platform.from_string(text)
    initial, periodicity = platform.spin_cycles_periodicity()
    nb_cycles = initial + ((1_000_000_000 - initial) % periodicity)
    for i in range(nb_cycles):
        platform.spin_cycle()
    return platform.total_load()


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
    print("Part 2", part2(puzzle_input))
