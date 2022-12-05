# https://adventofcode.com/2022/day/5

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


MOVE_RE = re.compile(r"move (?P<count>\d+) from (?P<source>\d) to (?P<dest>\d)")


def part1(text: str) -> str:
    stack_lines, move_lines = split_at(text.splitlines(), lambda line: line == "")
    stacks = init_stacks(stack_lines)
    apply_moves(stacks, move_lines)
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


def apply_moves(stacks, move_lines):
    for line in move_lines:
        match = MOVE_RE.match(line)
        assert match is not None
        source = int(match.group("source"))
        dest = int(match.group("dest"))
        for _ in range(int(match.group("count"))):
            crate = stacks[source].pop()
            stacks[dest].append(crate)


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
