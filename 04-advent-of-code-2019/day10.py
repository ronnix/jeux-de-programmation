from collections import defaultdict
from heapq import heappop, heappush
from math import atan2, pi
from textwrap import dedent
from typing import NamedTuple

from more_itertools import nth

import pytest


def sign(n):
    return 1 if n > 0 else -1 if n < 0 else 0


class Vector(NamedTuple):
    x: int
    y: int

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def squared_norm(self):
        return self.x ** 2 + self.y ** 2

    def angle(self):
        angle = atan2(self.y, self.x) + (pi / 2.0)
        while angle < 0.0:
            angle += 2.0 * pi
        while angle > 2.0 * pi:
            angle -= 2.0 * pi
        return angle


def test_count_observable_asteroids():
    asteroids = build_asteroid_map(
        dedent(
            """\
            .#..#
            .....
            #####
            ....#
            ...##"""
        )
    )
    counts = {
        (k.x, k.y): len(v) for k, v in count_observable_asteroids(asteroids).items()
    }
    assert counts == {
        (0, 2): 6,
        (1, 0): 7,
        (1, 2): 7,
        (2, 2): 7,
        (3, 2): 7,
        (3, 4): 8,
        (4, 0): 7,
        (4, 2): 5,
        (4, 3): 7,
        (4, 4): 7,
    }


@pytest.mark.parametrize(
    "data,count,pos",
    [
        (
            dedent(
                """\
                .#..#
                .....
                #####
                ....#
                ...##"""
            ),
            8,
            Vector(3, 4),
        ),
        (
            dedent(
                """\
                ......#.#.
                #..#.#....
                ..#######.
                .#.#.###..
                .#..#.....
                ..#....#.#
                #..#....#.
                .##.#..###
                ##...#..#.
                .#....####"""
            ),
            33,
            Vector(5, 8),
        ),
        (
            dedent(
                """\
                #.#...#.#.
                .###....#.
                .#....#...
                ##.#.#.#.#
                ....#.#.#.
                .##..###.#
                ..#...##..
                ..##....##
                ......#...
                .####.###."""
            ),
            35,
            Vector(1, 2),
        ),
        (
            dedent(
                """\
                .#..#..###
                ####.###.#
                ....###.#.
                ..###.##.#
                ##.##.#.#.
                ....###..#
                ..#.#..#.#
                #..#.#.###
                .##...##.#
                .....#.#.."""
            ),
            41,
            Vector(6, 3),
        ),
        (
            dedent(
                """\
                .#..##.###...#######
                ##.############..##.
                .#.######.########.#
                .###.#######.####.#.
                #####.##.#.##.###.##
                ..#####..#.#########
                ####################
                #.####....###.#.#.##
                ##.#################
                #####.##.###..####..
                ..######..##.#######
                ####.##.####...##..#
                .#####..#.######.###
                ##...#.##########...
                #.##########.#######
                .####.#.###.###.#.##
                ....##.##.###..#####
                .#.#.###########.###
                #.#.#.#####.####.###
                ###.##.####.##.#..##"""
            ),
            210,
            Vector(11, 13),
        ),
    ],
)
def test_max_observable_asteroids(data, count, pos):
    asteroids = build_asteroid_map(data)
    assert max_observable_asteroids(asteroids) == (count, pos)


def part1(asteroids):
    return max_observable_asteroids(asteroids)


def count_observable_asteroids(asteroids):
    return {pos: observable_from(pos, asteroids) for pos in asteroids}


def observable_from(pos, asteroids):
    observable = defaultdict(list)
    for asteroid in asteroids - {pos}:
        looking_to_asteroid = asteroid - pos
        angle = looking_to_asteroid.angle()
        distance = looking_to_asteroid.squared_norm()
        heappush(observable[angle], (distance, asteroid))
    return observable


def max_observable_asteroids(asteroids):
    return max(
        (len(targets), pos)
        for pos, targets in count_observable_asteroids(asteroids).items()
    )


def build_asteroid_map(data):
    def _asteroid_positions():
        for y, line in enumerate(data.splitlines()):
            for x, char in enumerate(line):
                if char == "#":
                    yield Vector(x, y)

    return set(_asteroid_positions())


def test_vaporization_order():
    asteroids = build_asteroid_map(
        dedent(
            """\
            .#....#####...#..
            ##...##.#####..##
            ##...#...#.#####.
            ..#.....X...###..
            ..#.#.....#....##"""
        )
    )
    laser_position = Vector(8, 3)
    assert list(vaporization_order(laser_position, asteroids)) == [
        (8, 1),
        (9, 0),
        (9, 1),
        (10, 0),
        (9, 2),
        (11, 1),
        (12, 1),
        (11, 2),
        (15, 1),
        (12, 2),
        (13, 2),
        (14, 2),
        (15, 2),
        (12, 3),
        (16, 4),
        (15, 4),
        (10, 4),
        (4, 4),
        (2, 4),
        (2, 3),
        (0, 2),
        (1, 2),
        (0, 1),
        (1, 1),
        (5, 2),
        (1, 0),
        (5, 1),
        (6, 1),
        (6, 0),
        (7, 0),
        (8, 0),
        (10, 1),
        (14, 0),
        (16, 1),
        (13, 3),
        (14, 3),
    ]


def vaporization_order(laser_position, asteroids):
    observable = observable_from(laser_position, asteroids)
    while any(len(targets) for targets in observable.values()):
        for angle, targets in sorted(observable.items()):
            if targets:
                distance, vector = heappop(targets)
                yield (vector.x, vector.y)


def part2(asteroids, laser_position):
    x, y = nth(vaporization_order(laser_position, asteroids), 199)
    return x * 100 + y


if __name__ == "__main__":
    with open("day10.txt") as file_:
        asteroids = build_asteroid_map(file_.read())
    count, position = part1(asteroids)
    print(f"Part 1:", count)
    print(f"Part 2:", part2(asteroids, position))
