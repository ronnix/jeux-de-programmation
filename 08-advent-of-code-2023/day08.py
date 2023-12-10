# https://adventofcode.com/2023/day/8
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from itertools import cycle
from typing import Dict, List, Tuple
import re

import pytest


EXAMPLE_MAP = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""


def test_parse_map():
    m = Map.from_string(EXAMPLE_MAP)
    assert m.instructions == [Direction.RIGHT, Direction.LEFT]
    assert m.network == {
        "AAA": ("BBB", "CCC"),
        "BBB": ("DDD", "EEE"),
        "CCC": ("ZZZ", "GGG"),
        "DDD": ("DDD", "DDD"),
        "EEE": ("EEE", "EEE"),
        "GGG": ("GGG", "GGG"),
        "ZZZ": ("ZZZ", "ZZZ"),
    }


def test_path():
    m = Map.from_string(EXAMPLE_MAP)
    assert m.path() == ["CCC", "ZZZ"]


class Direction(IntEnum):
    LEFT = 0
    RIGHT = 1

    @classmethod
    def from_char(cls, c: str) -> Direction:
        match c:
            case "L":
                return cls.LEFT
            case "R":
                return cls.RIGHT
            case other:
                raise ValueError


Node = str


@dataclass
class Map:
    instructions: List[Direction]
    network: Dict[Node, Tuple[Node, Node]]

    @classmethod
    def from_string(cls, text: str) -> Map:
        lines = text.splitlines()
        return cls(
            instructions=[Direction.from_char(char) for char in lines[0]],
            network=dict(cls.parse_node(line) for line in lines[2:] if line),
        )

    @classmethod
    def parse_node(cls, line: str) -> Tuple[Node, Tuple[Node, Node]]:
        mo = re.match(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", line)
        assert mo is not None
        return (mo.group(1), (mo.group(2), mo.group(3)))

    def path(self, origin: Node = "AAA", destination: Node = "ZZZ") -> List[Node]:
        node = origin
        result = []
        instructions = cycle(self.instructions)
        while node != destination:
            node = self.network[node][next(instructions)]
            result.append(node)
        return result


def test_part1():
    assert part1(EXAMPLE_MAP) == 2


def part1(text: str) -> int:
    m = Map.from_string(text)
    return len(m.path())


def read_puzzle_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
