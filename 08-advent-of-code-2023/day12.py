# https://adventofcode.com/2023/day/12
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterator

from more_itertools import ilen
import pytest


EXAMPLE = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def test_parse_record():
    assert Record.from_string("???.### 1,1,3") == Record(
        conditions="???.###", group_lengths=[1, 1, 3]
    )


def test_regex():
    assert (
        Record.from_string("???.### 1,1,3").regex()
        == r"^[\.\?]*[#\?]{1}[\.\?]+[#\?]{1}[\.\?]+[#\?]{3}[\.\?]*$"
    )


@pytest.mark.parametrize(
    "s,res",
    [
        ("", []),
        (".", ["."]),
        ("#", ["#"]),
        ("..", [".."]),
        ("##", ["##"]),
        ("#.#.###", ["#.#.###"]),
        (
            "???.###",
            [
                "....###",
                "..#.###",
                ".#..###",
                ".##.###",
                "#...###",
                "#.#.###",
                "##..###",
                "###.###",
            ],
        ),
    ],
)
def test_expand(s, res):
    assert list(expand(s)) == res


def expand(pattern: str) -> Iterator[str]:
    if len(pattern) == 0:
        return

    first = pattern[0]
    rest = pattern[1:]

    for possible_first in [".", "#"] if first == "?" else first:
        if rest:
            for possible_rest in expand(rest):
                yield possible_first + possible_rest
        else:
            yield possible_first


@pytest.mark.parametrize(
    "s, res",
    [
        ("???.### 1,1,3", 1),
        (".??..??...?##. 1,1,3", 4),
        ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
        ("????.#...#... 4,1,1", 1),
        ("????.######..#####. 1,6,5", 4),
        ("?###???????? 3,2,1", 10),
    ],
)
def test_number_of_possible_arrangements(s, res):
    record = Record.from_string(s)
    assert record.number_of_possible_arrangements() == res


@dataclass(frozen=True)
class Record:
    conditions: str
    group_lengths: list[int]

    @classmethod
    def from_string(cls, text: str) -> Record:
        left, right = text.split(" ")
        return cls(conditions=left, group_lengths=[int(s) for s in right.split(",")])

    def number_of_possible_arrangements(self) -> int:
        regex = re.compile(self.regex())
        return ilen(
            variant for variant in expand(self.conditions) if regex.match(variant)
        )

    def regex(self) -> str:
        OPERATIONAL = r"[\.\?]"
        BROKEN = r"[#\?]"
        return (
            "^"
            + OPERATIONAL
            + "*"
            + (OPERATIONAL + "+").join(
                BROKEN + "{" + str(n) + "}" for n in self.group_lengths
            )
            + OPERATIONAL
            + "*"
            + "$"
        )


def test_part1():
    assert part1(EXAMPLE) == 21


def part1(text: str) -> int:
    records = [Record.from_string(line) for line in text.splitlines() if line]
    return sum(record.number_of_possible_arrangements() for record in records)


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
