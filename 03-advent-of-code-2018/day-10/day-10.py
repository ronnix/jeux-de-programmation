#!/usr/bin/env python
import re
from textwrap import dedent
from typing import NamedTuple


def main():
    with open("input.txt") as stream:
        points = list(read_input(stream))

    min_surface, min_surface_time = minimize_surface(Grid(points))
    print(f"Point configuration has minimal surface {min_surface} after {min_surface_time} seconds")

    print("\nHere is the message:\n")
    print(Grid(points).move(min_surface_time))


def read_input(stream):
    return (Point.from_string(line) for line in stream if line.strip())


class Point(NamedTuple):
    x: int
    y: int
    vx: int
    vy: int

    @classmethod
    def from_string(cls, s):
        return cls(*map(int, cls.POINT_RE.match(s).groups()))

    POINT_RE = re.compile(
        r"position=<\s*(-?\d+),\s+(-?\d+)> velocity=<\s*(-?\d+),\s+(-?\d+)>"
    )

    def move(self, seconds=1):
        return Point(
            x=self.x + self.vx * seconds,
            y=self.y + self.vy * seconds,
            vx=self.vx,
            vy=self.vy,
        )


class Grid:
    def __init__(self, points):
        self.points = tuple(points)

    def move(self, seconds=1):
        self.points = tuple(point.move(seconds) for point in self.points)
        return self

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points
        self._grid = {(p.x, p.y) for p in self._points}
        self.min_x = min(x for (x, _) in self._grid)
        self.max_x = max(x for (x, _) in self._grid)
        self.min_y = min(y for (_, y) in self._grid)
        self.max_y = max(y for (_, y) in self._grid)
        self.width = self.max_x - self.min_x + 1
        self.height = self.max_y - self.min_y + 1

    def __str__(self):
        return "\n".join(
            "".join(
                "#" if (x, y) in self._grid else "."
                for x in range(self.min_x, self.max_x + 1)
            )
            for y in range(self.min_y, self.max_y + 1)
        )


def minimize_surface(grid, max_time=12000):
    initial_surface = grid.width * grid.height

    min_surface = None
    min_surface_time = None
    time = 0
    while time < max_time:
        surface = grid.width * grid.height
        if min_surface is None or surface < min_surface:
            min_surface = surface
            min_surface_time = time
        time += 1
        grid.move()
    return min_surface, min_surface_time


SAMPLE_INPUT = """\
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
"""


def test_to_string():
    stream = SAMPLE_INPUT.splitlines()
    points = list(read_input(stream))
    grid = Grid(points)
    assert str(grid) == dedent(
        """\
        ........#.............
        ................#.....
        .........#.#..#.......
        ......................
        #..........#.#.......#
        ...............#......
        ....#.................
        ..#.#....#............
        .......#..............
        ......#...............
        ...#...#.#...#........
        ....#..#..#.........#.
        .......#..............
        ...........#..#.......
        #...........#.........
        ...#.......#.........."""
    )


def test_move():
    stream = SAMPLE_INPUT.splitlines()
    points = list(read_input(stream))
    grid = Grid(points)
    assert str(grid.move(3)) == dedent(
        """\
        #...#..###
        #...#...#.
        #...#...#.
        #####...#.
        #...#...#.
        #...#...#.
        #...#...#.
        #...#..###"""
    )


def test_minimize_surface():
    stream = SAMPLE_INPUT.splitlines()
    points = list(read_input(stream))
    grid = Grid(points)
    assert minimize_surface(grid, max_time=10) == (80, 3)


if __name__ == "__main__":
    main()
