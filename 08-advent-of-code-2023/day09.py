# https://adventofcode.com/2023/day/9
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from more_itertools import pairwise

import pytest


EXAMPLE_REPORT = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def test_parse_report():
    assert Sequence.from_list(EXAMPLE_REPORT) == [
        Sequence([0, 3, 6, 9, 12, 15]),
        Sequence([1, 3, 6, 10, 15, 21]),
        Sequence([10, 13, 16, 21, 30, 45]),
    ]


def test_differences():
    assert Sequence([0, 3, 6, 9, 12, 15]).differences() == Sequence([3, 3, 3, 3, 3])
    assert Sequence([3, 3, 3, 3, 3]).differences() == Sequence([0, 0, 0, 0])


@pytest.mark.parametrize(
    "values, next_value",
    [
        ([0, 3, 6, 9, 12, 15], 18),
        ([1, 3, 6, 10, 15, 21], 28),
        ([10, 13, 16, 21, 30, 45], 68),
    ],
)
def test_predict_next(values, next_value):
    assert Sequence(values).predict_next() == next_value


@dataclass(frozen=True)
class Sequence:
    values: List[int]

    @classmethod
    def from_list(cls, text: str) -> List[Sequence]:
        return [
            cls(values=[int(s) for s in line.split(" ")])
            for line in text.splitlines()
            if line
        ]

    def differences(self) -> Sequence:
        return Sequence(values=[x2 - x1 for x1, x2 in pairwise(self.values)])

    def predict_next(self) -> int:
        if all(v == 0 for v in self.values):
            return 0
        else:
            return self.values[-1] + self.differences().predict_next()


def test_part1():
    assert part1(EXAMPLE_REPORT) == 114


def part1(text: str) -> int:
    return sum(sequence.predict_next() for sequence in Sequence.from_list(text))


def read_puzzle_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
