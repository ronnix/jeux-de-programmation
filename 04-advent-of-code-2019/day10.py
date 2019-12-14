from collections import defaultdict
from heapq import heappop, heappush
from math import atan2, pi
from textwrap import dedent
from typing import NamedTuple

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
    count, _ = max_observable_asteroids(asteroids)
    return count


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


if __name__ == "__main__":
    with open("day10.txt") as file_:
        asteroids = build_asteroid_map(file_.read())
    print(f"Part 1:", part1(asteroids))
