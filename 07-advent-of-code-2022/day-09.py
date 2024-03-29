# https://adventofcode.com/2022/day/9

from __future__ import annotations

from enum import StrEnum
from typing import List, NamedTuple, Set

import pytest


EXAMPLE_INPUT = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""


# === Part 1 ===


def test_part1():
    assert part1(EXAMPLE_INPUT) == 13


def test_head_motion():
    rope = Rope()
    rope.apply_motions(EXAMPLE_INPUT.splitlines())
    assert rope.head == Position(2, -2)


def test_tail_motion():
    rope = Rope()
    lines = EXAMPLE_INPUT.splitlines()
    expected_tail_positions = [
        Position(3, 0),
        Position(4, -3),
    ]
    for line, position in zip(lines, expected_tail_positions):
        rope.apply_motions([line])
        assert rope.tail == position


class Direction(StrEnum):
    L = "L"
    R = "R"
    U = "U"
    D = "D"


class Motion(NamedTuple):
    direction: Direction
    steps: int

    @classmethod
    def from_string(cls, s: str) -> "Motion":
        direction, steps = s.split()
        return cls(Direction(direction), int(steps))


class Position(NamedTuple):
    x: int
    y: int

    def move(self, direction: Direction) -> "Position":
        match direction:
            case Direction.L:
                return Position(self.x - 1, self.y)
            case Direction.R:
                return Position(self.x + 1, self.y)
            case Direction.U:
                return Position(self.x, self.y - 1)
            case Direction.D:
                return Position(self.x, self.y + 1)

    def follow(self, target: "Position") -> "Position":
        xdist = target.x - self.x
        ydist = target.y - self.y

        touching = abs(xdist) <= 1 and abs(ydist) <= 1
        if touching:
            return self

        xstep = xdist // abs(xdist) if xdist else 0
        ystep = ydist // abs(ydist) if ydist else 0

        return Position(self.x + xstep, self.y + ystep)


@pytest.mark.parametrize(
    "head,tail,expected",
    [
        ((2, 1), (1, 1), (1, 1)),
        ((1, 1), (2, 2), (2, 2)),
        ((1, 1), (1, 1), (1, 1)),
        ((3, 1), (1, 1), (2, 1)),
        ((1, 3), (1, 1), (1, 2)),
        ((2, 1), (1, 3), (2, 2)),
    ],
)
def test_follow(head, tail, expected):
    assert Position(*tail).follow(Position(*head)) == Position(*expected)


class Rope:
    knots: List[Position]
    visited_by_tail: Set[Position]

    def __init__(self, nb_knots=2):
        self.knots = [Position(0, 0)] * nb_knots
        self.visited_by_tail = {self.tail}

    @property
    def head(self):
        return self.knots[0]

    @property
    def tail(self):
        return self.knots[-1]

    def apply_motions(self, lines) -> None:
        for line in lines:
            motion = Motion.from_string(line)
            for _ in range(motion.steps):
                prev_knot = None
                for i in range(len(self.knots)):
                    if prev_knot is None:
                        prev_knot = self.knots[i] = self.knots[i].move(motion.direction)
                    else:
                        prev_knot = self.knots[i] = self.knots[i].follow(prev_knot)
                self.visited_by_tail.add(self.tail)


def part1(text: str) -> int:
    rope = Rope()
    rope.apply_motions(text.splitlines())
    return len(rope.visited_by_tail)


# === Part 2 ===


def test_part2():
    assert part2(EXAMPLE_INPUT) == 1


LARGER_EXAMPLE = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""


def test_part2_larger_example():
    assert part2(LARGER_EXAMPLE) == 36


def part2(text: str) -> int:
    rope = Rope(nb_knots=10)
    rope.apply_motions(text.splitlines())
    return len(rope.visited_by_tail)


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
    print("Part 2:", part2(text))
