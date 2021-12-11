# https://adventofcode.com/2021/day/11

import itertools
from textwrap import dedent
from typing import Iterator, List, Tuple

import numpy as np


SAMPLE_INPUT = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


# === Part 1 ===

Point = Tuple[int, int]

NEIGHBORS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]


class Grid:
    def __init__(self, numbers: List[List[int]]) -> None:
        self.array = np.array(numbers)
        self.height = self.array.shape[0]
        self.width = self.array.shape[1]

    def at(self, x: int, y: int) -> int:
        return self.array[y, x]

    def step(self) -> int:
        # 1. Increase energy level of all octopuses
        self.array += np.ones(self.array.shape, np.int64)

        # 2. Flash any octopus that has energy greater than 9
        flashed = set()
        to_flash = set(self.greater_than_nine())
        while to_flash:
            x, y = to_flash.pop()
            flashed.add((x, y))
            for nx, ny in self.neighbors(x, y):
                self.array[ny, nx] += 1
                if self.at(nx, ny) > 9 and (nx, ny) not in flashed:
                    to_flash.add((nx, ny))

        # 3. Any octopus that flashed goes back to zero
        for fx, fy in flashed:
            self.array[fy, fx] = 0

        return len(flashed)

    def greater_than_nine(self) -> Iterator[Point]:
        for y in range(self.height):
            for x in range(self.width):
                if self.at(x, y) > 9:
                    yield (x, y)

    def neighbors(self, x: int, y: int) -> Iterator[Point]:
        for (dx, dy) in NEIGHBORS:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= self.width:
                continue
            if ny < 0 or ny >= self.height:
                continue
            if nx == x and ny == y:
                continue
            yield (nx, ny)


def test_sample_grid() -> None:
    grid = parse(SAMPLE_INPUT)
    assert grid.width == 10
    assert grid.height == 10
    assert grid.at(0, 0) == 5
    assert grid.at(9, 9) == 6


def test_step() -> None:
    grid = parse(SAMPLE_INPUT)
    nb_flashed = grid.step()
    assert nb_flashed == 0
    after_step_1 = parse(
        dedent(
            """\
            6594254334
            3856965822
            6375667284
            7252447257
            7468496589
            5278635756
            3287952832
            7993992245
            5957959665
            6394862637"""
        )
    )
    assert np.all(grid.array == after_step_1.array)
    nb_flashed = grid.step()
    assert nb_flashed == 35
    after_step_2 = parse(
        dedent(
            """\
            8807476555
            5089087054
            8597889608
            8485769600
            8700908800
            6600088989
            6800005943
            0000007456
            9000000876
            8700006848"""
        )
    )
    assert np.all(grid.array == after_step_2.array)


def test_count_flashes() -> None:
    grid = parse(SAMPLE_INPUT)
    assert count_flashes(grid, 10) == 204


def count_flashes(grid: Grid, steps: int) -> int:
    return sum(grid.step() for _ in range(steps))


def part1(grid: Grid) -> int:
    return count_flashes(grid, 100)


# === Part 2 ===


def test_how_many_steps_before_all_octopuses_flash() -> None:
    grid = parse(SAMPLE_INPUT)
    assert how_many_steps_before_all_octopuses_flash(grid) == 195


def how_many_steps_before_all_octopuses_flash(grid: Grid) -> int:
    for n in itertools.count(1):
        nb_flashed = grid.step()
        if nb_flashed == 100:
            return n
    raise RuntimeError  # never happens


def part2(grid: Grid) -> int:
    return how_many_steps_before_all_octopuses_flash(grid)


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> Grid:
    return Grid([[int(char) for char in line] for line in text.splitlines()])


if __name__ == "__main__":
    print("Part 1:", part1(parse(read_input())))
    print("Part 2:", part2(parse(read_input())))
