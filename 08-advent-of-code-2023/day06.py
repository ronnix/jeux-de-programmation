# https://adventofcode.com/2023/day/6
from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from math import ceil, floor, sqrt
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
        # We solve the equation "x * (b - x) > C" => "b.x - x^2 > c" => "x^2 - b.x + c < 0"
        # where a = 1,  b = -time and c = distance to find the two values of x where the
        # distance is equal to the distance.

        delta = (self.time**2) - 4 * self.distance  # delta = b^2 - 4.a.c
        assert delta > 0
        s1 = (self.time - sqrt(delta)) / 2
        s2 = (self.time + sqrt(delta)) / 2

        # Those are floating point numbers, now we want :
        # - the smallest integer time value at which we start beat the record
        # - the largest integer time value at which we still beat the record
        smallest = floor(s1 + 1)
        largest = ceil(s2 - 1)

        # How many ways in this range?
        return largest - smallest + 1


def test_part1():
    assert part1(EXAMPLE) == 288


def part1(text: str) -> int:
    races = Race.parse(text)
    return product(race.nb_ways_to_win() for race in races)


def test_part2():
    assert part2(EXAMPLE) == 71503


def part2(text: str) -> int:
    races = Race.parse(text.replace(" ", ""))
    return product(race.nb_ways_to_win() for race in races)


def product(values: Iterable[int]) -> int:
    return reduce(operator.mul, values, 1)


def read_puzzle_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
    print("Part 2", part2(puzzle_input))
