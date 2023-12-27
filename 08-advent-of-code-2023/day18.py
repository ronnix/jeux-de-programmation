# https://adventofcode.com/2023/day/18
#
# I struggled a lot on this one, which was similar to day 10 part 2, on which I had given up.
#
# I tried to solve it on my own first, attempting to use the raycasting / point-in-polygon
# method of counting the number of polygon boundary crossings, but like day 10, I was unsuccessful.
#
# So I took it as an opportunity for learning and started reading some hints.
#
# First I learned about the shoelace formula for computing the area of a polygon, but this
# was not enough, because it does not take into account the area of the edge "pixels".
#
# I was stuck, so I looked for help again, and read about a clever way of combining
# the result of the shoelace formula with Pick's method (whih I did not know about
# either) to compute the total area of the trench.
#
from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from itertools import pairwise
from typing import NamedTuple, Self
import re

import pytest

from grid import Coords, Direction


EXAMPLE = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""


def test_parse_instructions():
    assert Instruction.from_string(EXAMPLE.splitlines()[0]) == Instruction(
        direction=Direction.RIGHT, length=6, color="#70c710"
    )


class Instruction(NamedTuple):
    direction: Direction
    length: int
    color: str

    @classmethod
    def from_string(cls, text: str) -> Self:
        mo = re.match(r"^([UDLR]) (\d+) \((#[0-9a-f]{6})\)$", text)
        assert mo is not None
        match mo.group(1):
            case "U":
                direction = Direction.UP
            case "D":
                direction = Direction.DOWN
            case "L":
                direction = Direction.LEFT
            case "R":
                direction = Direction.RIGHT
        return cls(direction=direction, length=int(mo.group(2)), color=mo.group(3))


class TestPolygon:
    @pytest.fixture
    def polygon(self):
        return Polygon.from_string(EXAMPLE)

    def test_number_of_points(self, polygon):
        assert len(polygon.points) == 15

    def test_back_to_where_we_started(self, polygon):
        assert polygon.points[0] == polygon.points[-1]

    def test_perimeter(self, polygon):
        assert polygon.perimeter == 38

    def test_sholace_area(self, polygon):
        assert polygon.shoelace_area == 42

    def test_area(self, polygon):
        assert polygon.area == 62


@dataclass
class Polygon:
    points: list[Coords]

    @classmethod
    def from_string(cls, text: str) -> Self:
        coords = Coords(0, 0)
        points = [coords]
        for instruction in (
            Instruction.from_string(line) for line in text.splitlines() if line
        ):
            coords += instruction.direction.value * instruction.length
            points.append(coords)
        return cls(points=points)

    @cached_property
    def perimeter(self) -> int:
        return sum(
            abs(p1.x - p2.x) + abs(p1.y - p2.y) for p1, p2 in pairwise(self.points)
        )

    @property
    def area(self) -> int:
        # The total area of the filled trench
        return self.inner_area + self.trench_area

    @property
    def inner_area(self) -> int:
        # Using Pick's theroem we can count how many squares are contained inside
        # that polygon, using its area and the perimeter
        return points_inside_polygon(self.shoelace_area, self.trench_area)

    @property
    def shoelace_area(self) -> int:
        # The shoelace formula gives us the area of the polygon defined by the centers
        # of each hole, so it does not take into account the whole area of the trench
        return sum(p1.x * p2.y - p2.x * p1.y for p1, p2 in pairwise(self.points)) // 2

    @property
    def trench_area(self) -> int:
        # The area of the trench is the number of hole on the polygon's perimeter
        return self.perimeter


def points_inside_polygon(polygon_area: int, points_on_polygon_sides: int) -> int:
    # pick's theorem
    return polygon_area - (points_on_polygon_sides // 2) + 1


def test_part1():
    assert part1(EXAMPLE) == 62


def part1(text: str) -> int:
    polygon = Polygon.from_string(text)
    return polygon.area


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
