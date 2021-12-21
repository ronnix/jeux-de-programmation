# https://adventofcode.com/2021/day/17

from typing import Iterator, Set, Tuple
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


def test_find_highest_y_position_that_reaches_target() -> None:
    target = parse(SAMPLE_INPUT)
    assert find_highest_y_position_that_reaches(target) == 45


def find_highest_y_position_that_reaches(target: Area) -> int:
    # Brute force
    results = (
        highest_y_position_for(vx, vy, target) for vx, vy in search_space(target)
    )
    return max(ymax for success, ymax in results if success)


def search_space(target: Area) -> Iterator[Tuple[int, int]]:
    xmin, xmax, ymin, ymax = target
    return itertools.product(range(xmax + 1), range(ymin, -ymin))


def test_highest_y_position_for() -> None:
    target = parse(SAMPLE_INPUT)
    success, ymax = highest_y_position_for(6, 9, target)
    assert success
    assert ymax == 45


def highest_y_position_for(vx: int, vy: int, target: Area) -> Tuple[bool, int]:
    state = ProbeState(vx=vx, vy=vy)
    ymax = state.y
    while not state.moved_past(target):
        state = state.next_state()
        if state.y > ymax:
            ymax = state.y
        if state.inside(target):
            return True, ymax
    return False, 0


def part1(target: Area) -> int:
    return find_highest_y_position_that_reaches(target)


# === Part 2 ===


def test_all_velocities() -> None:
    target = parse(SAMPLE_INPUT)
    assert set(all_velocities(target)) == {
        (23, -10),
        (25, -9),
        (27, -5),
        (29, -6),
        (22, -6),
        (21, -7),
        (9, 0),
        (27, -7),
        (24, -5),
        (25, -7),
        (26, -6),
        (25, -5),
        (6, 8),
        (11, -2),
        (20, -5),
        (29, -10),
        (6, 3),
        (28, -7),
        (8, 0),
        (30, -6),
        (29, -8),
        (20, -10),
        (6, 7),
        (6, 4),
        (6, 1),
        (14, -4),
        (21, -6),
        (26, -10),
        (7, -1),
        (7, 7),
        (8, -1),
        (21, -9),
        (6, 2),
        (20, -7),
        (30, -10),
        (14, -3),
        (20, -8),
        (13, -2),
        (7, 3),
        (28, -8),
        (29, -9),
        (15, -3),
        (22, -5),
        (26, -8),
        (25, -8),
        (25, -6),
        (15, -4),
        (9, -2),
        (15, -2),
        (12, -2),
        (28, -9),
        (12, -3),
        (24, -6),
        (23, -7),
        (25, -10),
        (7, 8),
        (11, -3),
        (26, -7),
        (7, 1),
        (23, -9),
        (6, 0),
        (22, -10),
        (27, -6),
        (8, 1),
        (22, -8),
        (13, -4),
        (7, 6),
        (28, -6),
        (11, -4),
        (12, -4),
        (26, -9),
        (7, 4),
        (24, -10),
        (23, -8),
        (30, -8),
        (7, 0),
        (9, -1),
        (10, -1),
        (26, -5),
        (22, -9),
        (6, 5),
        (7, 5),
        (23, -6),
        (28, -10),
        (10, -2),
        (11, -1),
        (20, -9),
        (14, -2),
        (29, -7),
        (13, -3),
        (23, -5),
        (24, -8),
        (27, -9),
        (30, -7),
        (28, -5),
        (21, -10),
        (7, 9),
        (6, 6),
        (21, -5),
        (27, -10),
        (7, 2),
        (30, -9),
        (21, -8),
        (22, -7),
        (24, -9),
        (20, -6),
        (6, 9),
        (29, -5),
        (8, -2),
        (27, -8),
        (30, -5),
        (24, -7),
    }


def all_velocities(target: Area) -> Set[Tuple[int, int]]:
    # Brute force
    results = (
        (vx, vy, highest_y_position_for(vx, vy, target)[0])
        for vx, vy in search_space(target)
    )
    return {(vx, vy) for vx, vy, success in results if success}


def part2(target: Area) -> int:
    return len(all_velocities(target))


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
    target = parse(read_input())
    print("Part 1:", part1(target))
    print("Part 2:", part2(target))
