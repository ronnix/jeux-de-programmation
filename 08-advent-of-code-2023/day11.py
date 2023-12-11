# https://adventofcode.com/2023/day/11
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from textwrap import dedent
from typing import Iterator, NamedTuple, Set, Tuple

import pytest


EXAMPLE_IMAGE = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def test_shortest_path():
    assert shortest_path(Coords(x=1, y=6), Coords(x=5, y=11)) == 9
    assert shortest_path(Coords(x=4, y=0), Coords(x=9, y=10)) == 15
    assert shortest_path(Coords(x=0, y=11), Coords(x=5, y=11)) == 5


def shortest_path(c1: Coords, c2: Coords) -> int:
    return abs(c1.x - c2.x) + abs(c1.y - c2.y)  # Manhattan distance


def test_expand():
    m = Map.from_string(EXAMPLE_IMAGE)
    assert str(m) == EXAMPLE_IMAGE
    assert str(m.expand()) == dedent(
        """\
        ....#........
        .........#...
        #............
        .............
        .............
        ........#....
        .#...........
        ............#
        .............
        .............
        .........#...
        #....#.......
        """
    )


class Coords(NamedTuple):
    x: int
    y: int


@dataclass(frozen=True)
class Map:
    width: int
    height: int
    galaxies: Set[Coords]

    def __str__(self):
        lines = []
        for y in range(self.height):
            line = (
                "".join(
                    "#" if Coords(x, y) in self.galaxies else "."
                    for x in range(self.width)
                )
                + "\n"
            )
            lines.append(line)
        return "".join(lines)

    @classmethod
    def from_string(cls, text: str) -> Map:
        galaxies = set()
        lines = [line for line in text.splitlines() if line]
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "#":
                    galaxies.add(Coords(x, y))
        return cls(width=len(lines[0]), height=len(lines), galaxies=galaxies)

    def expand(self, expansion_factor: int = 2) -> Map:
        y_offset, galaxies = self.expand_y(self.galaxies, expansion_factor)
        x_offset, galaxies = self.expand_x(galaxies, expansion_factor)
        return Map(
            width=self.width + x_offset,
            height=self.height + y_offset,
            galaxies=galaxies,
        )

    def expand_y(
        self, galaxies: Set[Coords], expansion_factor: int
    ) -> Tuple[int, Set[Coords]]:
        y_offset = 0
        new_galaxies = set()

        by_y = defaultdict(set)
        for galaxy in galaxies:
            by_y[galaxy.y].add(galaxy)

        for y in range(self.height):
            galaxies_in_line = by_y[y]
            if galaxies_in_line:
                for galaxy in galaxies_in_line:
                    new_galaxies.add(Coords(galaxy.x, galaxy.y + y_offset))
            else:
                print(f"No galaxies in line {y}")
                y_offset += expansion_factor - 1
        return y_offset, new_galaxies

    def expand_x(
        self, galaxies: Set[Coords], expansion_factor: int
    ) -> Tuple[int, Set[Coords]]:
        x_offset = 0
        new_galaxies = set()

        by_x = defaultdict(set)
        for galaxy in galaxies:
            by_x[galaxy.x].add(galaxy)

        for x in range(self.width):
            galaxies_in_column = by_x[x]
            if galaxies_in_column:
                for galaxy in galaxies_in_column:
                    new_galaxies.add(Coords(galaxy.x + x_offset, galaxy.y))
            else:
                print(f"No galaxies in column {x}")
                x_offset += expansion_factor - 1
        return x_offset, new_galaxies


def test_part1():
    assert part1(EXAMPLE_IMAGE) == 374


def part1(text: str) -> int:
    m = Map.from_string(text)
    return sum_of_shortest_paths(m, expansion_factor=2)


def sum_of_shortest_paths(m: Map, expansion_factor: int = 2) -> int:
    return sum(
        shortest_path(g1, g2)
        for g1, g2 in combinations(m.expand(expansion_factor).galaxies, 2)
    )


def test_part2():
    m = Map.from_string(EXAMPLE_IMAGE)
    assert sum_of_shortest_paths(m, expansion_factor=10) == 1030
    assert sum_of_shortest_paths(m, expansion_factor=100) == 8410


def part2(text: str) -> int:
    m = Map.from_string(text)
    return sum_of_shortest_paths(m, expansion_factor=1_000_000)


def read_puzzle_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
    print("Part 2", part2(puzzle_input))
