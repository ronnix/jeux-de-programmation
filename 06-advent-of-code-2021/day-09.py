# https://adventofcode.com/2021/day/9

import operator
from functools import reduce
from typing import Iterable, Iterator, List, Set, Tuple

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


Point = Tuple[int, int]


class HeightMap:
    def __init__(self, numbers: List[List[int]]) -> None:
        self.array = np.array(numbers)
        self.height = self.array.shape[0]
        self.width = self.array.shape[1]

    def sum_of_risk_levels(self) -> int:
        return sum(1 + self.at(x, y) for x, y in self.low_points())

    def at(self, x: int, y: int) -> int:
        return self.array[y, x]

    def low_points(self) -> Iterator[Point]:
        for x in range(self.width):
            for y in range(self.height):
                if self.is_low_point(x, y):
                    yield (x, y)

    def is_low_point(self, x: int, y: int) -> bool:
        return self.at(x, y) < min(self.at(nx, ny) for nx, ny in self.neighbors(x, y))

    def neighbors(self, x: int, y: int) -> Iterator[Point]:
        for (dx, dy) in {LEFT, RIGHT, UP, DOWN}:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= self.width:
                continue
            if ny < 0 or ny >= self.height:
                continue
            if nx == x and ny == y:
                continue
            yield (nx, ny)

    def basins(self) -> Iterator[Set[Point]]:
        for point in self.low_points():
            yield set(self.basin(point))

    def basin(self, point: Point) -> Iterable[Point]:
        value = self.at(*point)
        if value == 9:
            return
        yield point
        for neighbor in self.neighbors(*point):
            if self.at(*neighbor) > value:
                yield from self.basin(neighbor)


# === Part 1 ===


def test_parsing() -> None:
    heightmap = parse(SAMPLE_INPUT)
    assert heightmap.at(0, 0) == 2
    assert heightmap.at(1, 0) == 1
    assert heightmap.at(0, 1) == 3


def test_neighbors() -> None:
    heightmap = parse(SAMPLE_INPUT)
    assert sorted(heightmap.at(nx, ny) for nx, ny in heightmap.neighbors(1, 0)) == [
        2,
        9,
        9,
    ]


def test_low_points() -> None:
    heightmap = parse(SAMPLE_INPUT)
    assert heightmap.is_low_point(1, 0)
    assert not heightmap.is_low_point(0, 0)
    assert set(heightmap.low_points()) == {(1, 0), (9, 0), (6, 4), (2, 2)}


def test_part1() -> None:
    assert part1(parse(SAMPLE_INPUT)) == 15


def part1(heightmap: HeightMap) -> int:
    return heightmap.sum_of_risk_levels()


# === Part 2 ===


def test_basin() -> None:
    heightmap = parse(SAMPLE_INPUT)
    assert set(heightmap.basin((1, 0))) == {(1, 0), (0, 0), (0, 1)}
    assert set(heightmap.basin((9, 0))) == {
        (9, 0),
        (8, 0),
        (7, 0),
        (6, 0),
        (5, 0),
        (6, 1),
        (8, 1),
        (9, 1),
        (9, 2),
    }
    assert set(heightmap.basin((2, 2))) == {
        (2, 1),
        (3, 1),
        (4, 1),
        (1, 2),
        (2, 2),
        (3, 2),
        (4, 2),
        (5, 2),
        (0, 3),
        (1, 3),
        (2, 3),
        (3, 3),
        (4, 3),
        (1, 4),
    }
    assert set(heightmap.basin((6, 4))) == {
        (7, 2),
        (6, 3),
        (7, 3),
        (8, 3),
        (5, 4),
        (6, 4),
        (7, 4),
        (8, 4),
        (9, 4),
    }


def test_part2() -> None:
    assert part2(parse(SAMPLE_INPUT)) == 1134


def part2(heightmap: HeightMap) -> int:
    top_sizes = sorted((len(basin) for basin in heightmap.basins()), reverse=True)
    return product(top_sizes[:3])


def product(values: Iterable[int]) -> int:
    return reduce(operator.mul, values, 1)


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> HeightMap:
    return HeightMap([[int(char) for char in line] for line in text.splitlines()])


if __name__ == "__main__":
    heightmap = parse(read_input())
    print("Part 1:", part1(heightmap))
    print("Part 2:", part2(heightmap))
