from itertools import product
from typing import NamedTuple

import pytest


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)


def parse_input(data):
    return [line.split(",") for line in data.splitlines()]


def build_segments(moves):
    origin = Point(0, 0)
    for move in moves:
        direction = move[0]
        amount = int(move[1:])
        if direction == "U":
            destination = origin + Point(0, amount)
        elif direction == "D":
            destination = origin + Point(0, -amount)
        elif direction == "L":
            destination = origin + Point(-amount, 0)
        elif direction == "R":
            destination = origin + Point(amount, 0)
        yield (origin, destination)
        origin = destination


def intersections(l1, l2):
    for s1, s2 in product(l1, l2):
        p = intersection(s1, s2)
        if p is not None and p != Point(0, 0):
            yield p


def intersection(s1, s2):
    o1, d1 = s1
    o2, d2 = s2
    if between(o2.x, o1.x, d1.x) and between(o1.y, o2.y, d2.y):
        return Point(o2.x, o1.y)
    if between(o1.x, o2.x, d2.x) and between(o2.y, o1.y, d1.y):
        return Point(o1.x, o2.y)
    return None


def between(value, boundary1, boundary2):
    return (boundary1 <= value <= boundary2) or (boundary2 <= value <= boundary1)


def part1(wire1, wire2):
    return min(p.manhattan_distance() for p in intersections(wire1, wire2))


def test_build_segments():
    assert list(build_segments(["U1", "D2", "L3", "R4"])) == [
        (Point(0, 0), Point(0, 1)),
        (Point(0, 1), Point(0, -1)),
        (Point(0, -1), Point(-3, -1)),
        (Point(-3, -1), Point(1, -1)),
    ]


def test_intersection():
    p = intersection((Point(0, 0), Point(0, 5)), (Point(-2, 4), Point(3, 4)))
    assert p == Point(0, 4)


def test_no_intersection():
    p = intersection((Point(0, 0), Point(0, 5)), (Point(-2, 6), Point(3, 6)))
    assert p is None


def test_intersections():
    wire1 = build_segments(["R8", "U5", "L5", "D3"])
    wire2 = build_segments(["U7", "R6", "D4", "L4"])
    assert set(intersections(wire1, wire2)) == {Point(3, 3), Point(6, 5)}


@pytest.mark.parametrize(
    "data,res",
    [
        ("R8,U5,L5,D3\nU7,R6,D4,L4", 6),
        (("R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83"), 159),
        (
            (
                "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\n"
                "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
            ),
            135,
        ),
    ],
)
def test_part1(data, res):
    wires = [build_segments(moves) for moves in parse_input(data)]
    assert part1(*wires) == res


if __name__ == "__main__":
    with open("day03.txt") as file_:
        wires = [build_segments(moves) for moves in parse_input(file_.read())]
    print("Part 1:", part1(*wires))
