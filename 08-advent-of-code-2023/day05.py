# https://adventofcode.com/2023/day/5
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import Dict, List, Optional, Tuple
import re



EXAMPLE_ALMANAC = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def test_range():
    r = Range(destination=50, source=98, length=2)
    assert r.map(97) is None
    assert r.map(98) == 50
    assert r.map(99) == 51
    assert r.map(100) is None

    r = Range(destination=52, source=50, length=48)
    assert r.map(49) is None
    assert r.map(50) == 52
    assert r.map(97) == 99
    assert r.map(98) is None


@dataclass(frozen=True)
class Range:
    destination: int
    source: int
    length: int

    def map(self, value: int) -> Optional[int]:
        d = value - self.source
        if 0 <= d < self.length:
            return self.destination + d
        return None


def test_map():
    m = Map(
        source="seed",
        destination="soil",
        ranges=[
            Range(destination=50, source=98, length=2),
            Range(destination=52, source=50, length=48),
        ],
    )
    assert m[79] == 81
    assert m[14] == 14
    assert m[55] == 57
    assert m[13] == 13


def test_parse_map():
    m = Map.from_string(
        dedent(
            """
            seed-to-soil map:
            50 98 2
            52 50 48
            """
        )
    )
    assert m.source == "seed"
    assert m.destination == "soil"
    assert m.ranges == [
        Range(destination=50, source=98, length=2),
        Range(destination=52, source=50, length=48),
    ]


@dataclass(frozen=True)
class Map:
    source: str
    destination: str
    ranges: List[Range]

    @classmethod
    def from_string(cls, text: str) -> Map:
        lines = [line for line in text.splitlines() if line]
        mo = re.match(r"(\w+)-to-(\w+) map:", lines[0])
        assert mo is not None
        return Map(
            source=mo.group(1),
            destination=mo.group(2),
            ranges=[Range(*(int(s) for s in line.split(" "))) for line in lines[1:]],
        )

    def __getitem__(self, value: int) -> int:
        for range_ in self.ranges:
            res = range_.map(value)
            if res is not None:
                return res
        return value


def test_almanac():
    almanac = Almanac.from_string(EXAMPLE_ALMANAC)
    assert almanac.seeds == [79, 14, 55, 13]
    assert set(almanac.maps.keys()) == {
        "seed",
        "fertilizer",
        "soil",
        "water",
        "light",
        "temperature",
        "humidity",
    }


def test_find_location():
    almanac = Almanac.from_string(EXAMPLE_ALMANAC)
    assert almanac.find_location(79) == 82
    assert almanac.find_location(14) == 43
    assert almanac.find_location(55) == 86
    assert almanac.find_location(13) == 35


@dataclass(frozen=True)
class Almanac:
    seeds: List[int]
    maps: Dict[str, Map]

    @classmethod
    def from_string(cls, text: str) -> Almanac:
        paragraphs = [p for p in text.split("\n\n") if p]
        seeds = [int(s) for s in paragraphs[0].split(": ")[1].split(" ")]
        maps = [Map.from_string(paragraph) for paragraph in paragraphs[1:]]
        return cls(
            seeds=seeds,
            maps={m.source: m for m in maps},
        )

    def map(self, item: int, kind: str) -> Tuple[int, str]:
        map_ = self.maps[kind]
        return map_[item], map_.destination

    def find_location(self, seed: int) -> int:
        value = seed
        kind = "seed"
        while kind != "location":
            value, kind = self.map(value, kind)
        return value


def test_part1():
    assert part1(EXAMPLE_ALMANAC) == 35


def part1(text: str) -> int:
    almanac = Almanac.from_string(text)
    return min(almanac.find_location(seed) for seed in almanac.seeds)


if __name__ == "__main__":
    puzzle_input = Path("day05.txt").read_text()
    print("Part 1", part1(puzzle_input))
