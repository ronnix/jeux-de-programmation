# https://adventofcode.com/2023/day/6
from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import Iterable, List
import operator
import re

import pytest


EXAMPLE = """\
Time:      7  15   30
Distance:  9  40  200
"""


def test_parse_races():
    races = Race.parse(EXAMPLE)
    assert races == [
        Race(time=7, distance=9),
        Race(time=15, distance=40),
        Race(time=30, distance=200),
    ]


@pytest.mark.parametrize(
    "time, distance, result",
    [
        (7, 9, 4),
        (15, 40, 8),
        (30, 200, 9),
    ],
)
def test_nb_ways_to_win(time, distance, result):
    race = Race(time, distance)
    assert race.nb_ways_to_win() == result


@dataclass(frozen=True)
class Race:
    time: int
    distance: int

    @classmethod
    def parse(cls, text: str) -> List[Race]:
        lines = text.splitlines()
        times = (int(s) for s in re.split(r"\s+", lines[0].split(":")[1].strip()))
        distances = (int(s) for s in re.split(r"\s+", lines[1].split(":")[1].strip()))
        return [Race(time, distance) for time, distance in zip(times, distances)]

    def nb_ways_to_win(self) -> int:
        res = 0
        for charge_time in range(self.time + 1):
            speed = charge_time
            remaining_time = self.time - charge_time
            distance = speed * remaining_time
            if distance > self.distance:
                res += 1
        return res


def test_part1():
    assert part1(EXAMPLE) == 288


def part1(text: str) -> int:
    races = Race.parse(text)
    return product(race.nb_ways_to_win() for race in races)


def product(values: Iterable[int]) -> int:
    return reduce(operator.mul, values, 1)


def read_puzzle_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
