# https://adventofcode.com/2022/day/8

from __future__ import annotations

from itertools import takewhile
from typing import Generator

from more_itertools import ilen, split_after


EXAMPLE_INPUT = """\
30373
25512
65332
33549
35390
"""


# === Part 1 ===


def test_part1():
    assert part1(EXAMPLE_INPUT) == 21


def part1(text: str) -> int:
    grid = Grid.from_string(text)
    return len(list(grid.visible_trees()))


class Grid:
    def __init__(self, matrix):
        self.matrix = matrix
        self.width = len(self.matrix[0]) if self.matrix else 0
        self.height = len(self.matrix)

    @classmethod
    def from_string(cls, text: str) -> Grid:
        return cls(matrix=[list(line) for line in text.splitlines()])

    def visible_trees(self) -> Generator:
        for y in range(self.height):
            for x in range(self.width):
                if self.is_visible(x, y):
                    yield (x, y)

    def is_visible(self, x: int, y: int) -> bool:
        return any(
            (
                self.is_visible_from_the_left(x, y),
                self.is_visible_from_the_right(x, y),
                self.is_visible_from_the_top(x, y),
                self.is_visible_from_the_bottom(x, y),
            )
        )

    def is_visible_from_the_left(self, x: int, y: int) -> bool:
        height = self.matrix[y][x]
        return (x == 0) or all(self.matrix[y][x2] < height for x2 in range(0, x))

    def is_visible_from_the_right(self, x: int, y: int) -> bool:
        height = self.matrix[y][x]
        return (x == self.width - 1) or all(
            self.matrix[y][x2] < height for x2 in range(x + 1, self.width)
        )

    def is_visible_from_the_top(self, x: int, y: int) -> bool:
        height = self.matrix[y][x]
        return (y == 0) or all(self.matrix[y2][x] < height for y2 in range(0, y))

    def is_visible_from_the_bottom(self, x: int, y: int) -> bool:
        height = self.matrix[y][x]
        return (y == self.height - 1) or all(
            self.matrix[y2][x] < height for y2 in range(y + 1, self.height)
        )

    def highest_scenic_score(self) -> int:
        return max(
            self.scenic_score(x, y)
            for y in range(self.height)
            for x in range(self.width)
        )

    def scenic_score(self, x: int, y: int) -> int:
        up = self.viewing_distance_up(x, y)
        left = self.viewing_distance_left(x, y)
        right = self.viewing_distance_right(x, y)
        down = self.viewing_distance_down(x, y)
        return up * left * right * down

    def viewing_distance_up(self, x: int, y: int) -> int:
        if y == 0:
            return 0
        tree_house_height = self.matrix[y][x]
        heights = (self.matrix[y2][x] for y2 in range(y - 1, -1, -1))
        return ilen(
            next(split_after(heights, lambda height: height >= tree_house_height, 1))
        )

    def viewing_distance_left(self, x: int, y: int) -> int:
        if x == 0:
            return 0
        tree_house_height = self.matrix[y][x]
        heights = list(self.matrix[y][x2] for x2 in range(x - 1, -1, -1))
        return ilen(
            next(split_after(heights, lambda height: height >= tree_house_height, 1))
        )

    def viewing_distance_right(self, x: int, y: int) -> int:
        if x == self.width - 1:
            return 0
        tree_house_height = self.matrix[y][x]
        heights = (self.matrix[y][x2] for x2 in range(x + 1, self.width))
        return ilen(
            next(split_after(heights, lambda height: height >= tree_house_height, 1))
        )

    def viewing_distance_down(self, x: int, y: int) -> int:
        if y == self.height - 1:
            return 0
        tree_house_height = self.matrix[y][x]
        heights = (self.matrix[y2][x] for y2 in range(y + 1, self.height))
        return ilen(
            next(split_after(heights, lambda height: height >= tree_house_height, 1))
        )


# === Part 2 ===


def test_part2():
    assert part2(EXAMPLE_INPUT) == 8


def test_viewing_distance():
    grid = Grid.from_string(EXAMPLE_INPUT)
    assert grid.scenic_score(2, 1) == 4
    assert grid.viewing_distance_up(2, 3) == 2
    assert grid.viewing_distance_left(2, 3) == 2
    assert grid.scenic_score(2, 3) == 8


def part2(text: str) -> int:
    grid = Grid.from_string(text)
    return grid.highest_scenic_score()


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
    print("Part 2:", part2(text))
