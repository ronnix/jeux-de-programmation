# https://adventofcode.com/2022/day/5

from __future__ import annotations

from collections import defaultdict
from typing import Iterable, List, NamedTuple
import re

from more_itertools import split_at


EXAMPLE_INPUT = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


# === Part 1 ===


def test_part1():
    assert part1(EXAMPLE_INPUT) == "CMZ"


def part1(text: str) -> str:
    return rearrange_crates(crane_class=CrateMover9000, text=text)


def rearrange_crates(crane_class: type, text: str) -> str:
    stacks_lines, move_lines = split_at(text.splitlines(), lambda line: line == "")
    crane = crane_class(stacks_lines)
    crane.apply_moves(Move.from_string(line) for line in move_lines)
    return crane.top_crates()


class CrateMover9000:
    def __init__(self, lines: List[str]):
        self.stacks = defaultdict(list)
        nb_stacks = self.count_stacks(lines)
        for line in lines[-2::-1]:
            for i in range(nb_stacks):
                char = line[i * 4 + 1]
                if char != " ":
                    self.stacks[i + 1].append(char)

    @staticmethod
    def count_stacks(lines: List[str]) -> int:
        return (len(lines[0]) + 1) // 4

    def apply_moves(self, moves: Iterable[Move]) -> None:
        for move in moves:
            self.apply_move(move)

    def apply_move(self, move: Move) -> None:
        crates = self.pick_up_crates(move.source, move.nb)
        self.stacks[move.dest].extend(crates)

    def pick_up_crates(self, source: int, nb: int) -> List[str]:
        # one by one
        return [self.stacks[source].pop() for _ in range(nb)]

    def top_crates(self) -> str:
        return "".join(stack[-1] for stack in self.stacks.values())


class Move(NamedTuple):
    nb: int
    source: int
    dest: int

    MOVE_RE = re.compile(r"move (?P<nb>\d+) from (?P<source>\d) to (?P<dest>\d)")  # type: ignore

    @classmethod
    def from_string(cls, s: str) -> Move:
        match = cls.MOVE_RE.match(s)
        if match is None:
            raise SyntaxError
        return cls(  # type: ignore
            nb=int(match.group("nb")),
            source=int(match.group("source")),
            dest=int(match.group("dest")),
        )


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


# === Part 2 ===


def test_part2():
    assert part2(EXAMPLE_INPUT) == "MCD"


def part2(text: str) -> str:
    return rearrange_crates(crane_class=CrateMover9001, text=text)


class CrateMover9001(CrateMover9000):
    def pick_up_crates(self, source: int, nb: int) -> List[str]:
        # multiple at once
        crates = super().pick_up_crates(source, nb)
        return crates[::-1]  # reverse list


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
    print("Part 2:", part2(text))
