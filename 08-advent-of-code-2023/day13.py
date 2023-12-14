# https://adventofcode.com/2023/day/13
from __future__ import annotations

from typing import Optional

import pytest

from grid import Grid


EXAMPLE_PATTERNS = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


@pytest.fixture
def example_patterns():
    return [Pattern.from_string(text) for text in EXAMPLE_PATTERNS.split("\n\n")]


def test_parse_patterns(example_patterns):
    assert len(example_patterns) == 2


def test_find_vertical_line_symmetry(example_patterns):
    assert example_patterns[0].find_vertical_line_symmetry() == 5
    assert example_patterns[1].find_vertical_line_symmetry() is None


def test_find_horizontal_line_symmetry(example_patterns):
    assert example_patterns[1].find_horizontal_line_symmetry() == 4
    assert example_patterns[0].find_horizontal_line_symmetry() is None


class Pattern(Grid):
    def find_vertical_line_symmetry(self) -> Optional[int]:
        for x in range(0, self.width - 1):
            max_width = min(x + 1, self.width - x - 1)
            differs = False
            for d in range(max_width):
                for y in range(self.height):
                    if self.at(x - d, y) != self.at(x + 1 + d, y):
                        differs = True
                        break
                if differs:
                    break
            if differs:
                continue
            return x + 1  # our arrays start at zero but column numbers start at 1
        return None

    def find_horizontal_line_symmetry(self) -> Optional[int]:
        for y in range(0, self.height - 1):
            max_height = min(y + 1, self.height - y - 1)
            differs = False
            for d in range(max_height):
                if self.lines[y - d] != self.lines[y + d + 1]:
                    differs = True
                    break
            if not differs:
                return y + 1  # our arrays start at zero but row numbers start at 1
        return None


def test_part1():
    assert part1(EXAMPLE_PATTERNS) == 405


def part1(text: str) -> int:
    res = 0
    for pattern in (Pattern.from_string(s) for s in text.split("\n\n")):
        if (column := pattern.find_vertical_line_symmetry()) is not None:
            res += column
        if (row := pattern.find_horizontal_line_symmetry()) is not None:
            res += 100 * row
    return res


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
