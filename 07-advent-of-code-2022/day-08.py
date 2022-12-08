# https://adventofcode.com/2022/day/8

from __future__ import annotations

from typing import Generator


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


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
