# https://adventofcode.com/2021/day/9

from typing import Iterator, List, Tuple

import numpy as np


SAMPLE_INPUT = """\
2199943210
3987894921
9856789892
8767896789
9899965678"""

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)


class HeightMap:
    def __init__(self, numbers: List[List[int]]) -> None:
        self.array = np.array(numbers)
        self.height = self.array.shape[0]
        self.width = self.array.shape[1]

    def sum_of_risk_levels(self) -> int:
        return sum(1 + self.at(x, y) for x, y in self.low_points())

    def at(self, x: int, y: int) -> int:
        return self.array[y, x]

    def low_points(self) -> Iterator[Tuple[int, int]]:
        for x in range(self.width):
            for y in range(self.height):
                if self.is_low_point(x, y):
                    yield (x, y)

    def is_low_point(self, x: int, y: int) -> bool:
        return self.at(x, y) < min(self.neighbors(x, y))

    def neighbors(self, x: int, y: int) -> Iterator[int]:
        for (dx, dy) in {LEFT, RIGHT, UP, DOWN}:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= self.width:
                continue
            if ny < 0 or ny >= self.height:
                continue
            if nx == x and ny == y:
                continue
            yield self.at(nx, ny)


# === Part 1 ===


def test_parsing() -> None:
    heightmap = parse(SAMPLE_INPUT)
    assert heightmap.at(0, 0) == 2
    assert heightmap.at(1, 0) == 1
    assert heightmap.at(0, 1) == 3


def test_neighbors() -> None:
    heightmap = parse(SAMPLE_INPUT)
    assert sorted(heightmap.neighbors(1, 0)) == [2, 9, 9]


def test_low_points() -> None:
    heightmap = parse(SAMPLE_INPUT)
    assert heightmap.is_low_point(1, 0)
    assert not heightmap.is_low_point(0, 0)
    assert set(heightmap.low_points()) == {(1, 0), (9, 0), (6, 4), (2, 2)}


def test_part1() -> None:
    assert part1(parse(SAMPLE_INPUT)) == 15


def part1(heightmap: HeightMap) -> int:
    return heightmap.sum_of_risk_levels()


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> HeightMap:
    return HeightMap([[int(char) for char in line] for line in text.splitlines()])


if __name__ == "__main__":
    heightmap = parse(read_input())
    print("Part 1:", part1(heightmap))
