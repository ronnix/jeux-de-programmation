# https://adventofcode.com/2022/day/5

from __future__ import annotations

from collections import defaultdict
from typing import List, NamedTuple
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


def part1(text: str) -> str:
    return move_crates(text)


def move_crates(text: str, multiple_at_once=False) -> str:
    stack_lines, move_lines = split_at(text.splitlines(), lambda line: line == "")
    stacks = init_stacks(stack_lines)
    apply_moves(stacks, move_lines, multiple_at_once)
    return "".join(stack[-1] for stack in stacks.values())


def init_stacks(lines):
    stacks = defaultdict(list)
    nb_stacks = count_stacks(lines)
    for line in lines[-2::-1]:
        for i in range(nb_stacks):
            char = line[i * 4 + 1]
            if char != " ":
                stacks[i + 1].append(char)
    return stacks


def count_stacks(lines: List[str]) -> int:
    return (len(lines[0]) + 1) // 4


def apply_moves(stacks, move_lines, multiple_at_once):
    for line in move_lines:
        move = Move.from_string(line)
        crates = [stacks[move.source].pop() for _ in range(move.nb)]
        if multiple_at_once:
            crates = reversed(crates)
        stacks[move.dest].extend(crates)


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


# === Part 2 ===


def test_part2():
    assert part2(EXAMPLE_INPUT) == "MCD"


def part2(text: str) -> str:
    return move_crates(text, multiple_at_once=True)


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
    print("Part 2:", part2(text))
