# https://adventofcode.com/2022/day/4

from __future__ import annotations

from typing import Iterable, List

from more_itertools import quantify


EXAMPLE_INPUT = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


# === Part 1 ===


def test_part1():
    assert part1(EXAMPLE_INPUT) == 2


def part1(text: str) -> int:
    return quantify(range_pairs(text), completely_overlap)


def range_pairs(text: str) -> Iterable[Iterable[Range]]:
    return (map(Range, line.split(",")) for line in text.splitlines())


class Range:
    def __init__(self, s: str):
        self.start, self.end = map(int, s.split("-"))

    def includes(self, other: Range) -> bool:
        return self.start <= other.start and self.end >= other.end

    def overlaps_with(self, other: Range) -> bool:
        return (other.start <= self.start <= other.end) or (
            self.start <= other.start <= self.end
        )


def completely_overlap(pair: Iterable[Range]) -> bool:
    first, second = pair
    return first.includes(second) or second.includes(first)


# === Part 2 ===


def test_part2():
    assert part2(EXAMPLE_INPUT) == 4


def part2(text: str) -> int:
    return quantify(range_pairs(text), overlap)


def overlap(pair: Iterable[Range]) -> bool:
    first, second = pair
    return first.overlaps_with(second)


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
    print("Part 2:", part2(text))
