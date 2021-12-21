# https://adventofcode.com/2021/day/17

from typing import Tuple
import itertools
import re


SAMPLE_INPUT = "target area: x=20..30, y=-10..-5"

Area = Tuple[int, int, int, int]


# === Part 1 ===


class ProbeState:
    def __init__(self, vx, vy, x=0, y=0):
        self.vx = vx
        self.vy = vy
        self.x = x
        self.y = y

    def next_state(self) -> "ProbeState":
        next_x = self.x + self.vx
        next_y = self.y + self.vy
        if self.vx > 0:
            next_vx = self.vx - 1
        elif self.vx < 0:
            next_vx = self.vx + 1
        else:
            next_vx = self.vx
        next_vy = self.vy - 1
        return ProbeState(vx=next_vx, vy=next_vy, x=next_x, y=next_y)

    def inside(self, target: Area) -> bool:
        xmin, xmax, ymin, ymax = target
        return (xmin <= self.x <= xmax) and (ymin <= self.y <= ymax)

    def moved_past(self, target: Area) -> bool:
        xmin, xmax, ymin, ymax = target
        return self.x > xmax and self.vx > 1 or self.y < ymin and self.vy < 0


def test_parse() -> None:
    assert parse(SAMPLE_INPUT) == (20, 30, -10, -5)


def test_example_trajectory_1() -> None:
    target = parse(SAMPLE_INPUT)
    state = ProbeState(vx=7, vy=2)
    for _ in range(7):
        assert not state.inside(target)
        state = state.next_state()
    assert state.inside(target)


def test_example_trajectory_2() -> None:
    target = parse(SAMPLE_INPUT)
    state = ProbeState(vx=6, vy=3)
    for _ in range(9):
        assert not state.inside(target)
        state = state.next_state()
    assert state.inside(target)


def test_example_trajectory_3() -> None:
    target = parse(SAMPLE_INPUT)
    state = ProbeState(vx=9, vy=0)
    for _ in range(4):
        assert not state.inside(target)
        state = state.next_state()
    assert state.inside(target)


def test_example_trajectory_4() -> None:
    target = parse(SAMPLE_INPUT)
    state = ProbeState(vx=17, vy=-4)
    for _ in range(2):
        assert not state.inside(target)
        state = state.next_state()
    assert not state.inside(target)
    assert state.moved_past(target)


def test_highest_y_position_that_reaches_target() -> None:
    target = parse(SAMPLE_INPUT)
    assert find_highest_y_position_that_reaches(target) == 45


def find_highest_y_position_that_reaches(target: Area) -> int:
    # Brute force
    xmin, xmax, ymin, ymax = target
    search_space = itertools.product(range(xmax), range(ymin, -ymin))
    return max(highest_y_position_for(vx, vy, target) for vx, vy in search_space)


def test_highest_y_position_for() -> None:
    target = parse(SAMPLE_INPUT)
    assert highest_y_position_for(6, 9, target) == 45


def highest_y_position_for(vx: int, vy: int, target: Area) -> int:
    state = ProbeState(vx=vx, vy=vy)
    ymax = state.y
    while not state.moved_past(target):
        state = state.next_state()
        if state.y > ymax:
            ymax = state.y
        if state.inside(target):
            return ymax
    return 0


def part1(target: Area) -> int:
    return find_highest_y_position_that_reaches(target)


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> Area:
    mo = re.match(r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", text)
    assert mo is not None
    coords = [int(n) for n in mo.groups()]
    return coords[0], coords[1], coords[2], coords[3]


if __name__ == "__main__":
    print("Part 1:", part1(parse(read_input())))
