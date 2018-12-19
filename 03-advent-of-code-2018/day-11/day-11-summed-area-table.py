#!/usr/bin/env python
"""
Using a summed-area table for fast sums over rectangles
"""
from contextlib import contextmanager
from functools import lru_cache
import time

import numpy as np
import pytest


@contextmanager
def timeit(label):
    start = time.monotonic()
    yield
    end = time.monotonic()
    print(f"{label}: {end - start:.2f}s")


def test_summed_area_table():
    sat = SummedAreaTable([[1, 2, 3], [3, 4, 5], [4, 5, 6]])
    assert (sat.summed == np.array([[1, 3, 6], [4, 10, 18], [8, 19, 33]])).all()
    assert sat.rectangle_sum(0, 0, 1, 1) == 4
    assert sat.rectangle_sum(0, 0, 2, 2) == 20


class SummedAreaTable:
    """
    cf. https://en.wikipedia.org/wiki/Summed_area_table
    """

    def __init__(self, values):
        self.summed = np.array(values).cumsum(axis=0).cumsum(axis=1)

    def rectangle_sum(self, x0, y0, x1, y1):
        a = self.summed[y0, x0] if x0 >= 0 and y0 >= 0 else 0
        b = self.summed[y0, x1] if y0 >= 0 else 0
        c = self.summed[y1, x0] if x0 >= 0 else 0
        d = self.summed[y1, x1]
        return d - b - c + a


class Grid:
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.sat = SummedAreaTable(
            [
                [self.cell_power_level(x, y) for x in range(1, 301)]
                for y in range(1, 301)
            ]
        )

    @lru_cache(maxsize=None)
    def cell_power_level(self, x, y):
        rack_id = x + 10
        power_level = rack_id * y
        power_level += self.serial_number
        power_level *= rack_id
        hundreds_digit = power_level // 100 % 10
        return hundreds_digit - 5

    def square_with_largest_power_level(self, min_size=3, max_size=3):
        return max(
            (self.square_power_level(x, y, size), (x, y), size)
            for size in range(min_size, max_size + 1)
            for x in range(1, 300 - size + 1)
            for y in range(1, 300 - size + 1)
        )

    def square_power_level(self, x, y, size):
        return self.sat.rectangle_sum(x - 2, y - 2, x + size - 2, y + size - 2)


@pytest.mark.parametrize(
    "serial_number, min_size, max_size, coords, size, total",
    [
        (18, 3, 3, (33, 45), 3, 29),
        (42, 3, 3, (21, 61), 3, 30),
        (18, 1, 300, (90, 269), 16, 113),
        (42, 1, 300, (232, 251), 12, 119),
    ],
)
def test_square_with_largest_power_level(
    serial_number, min_size, max_size, coords, size, total
):
    grid = Grid(serial_number)
    assert grid.square_with_largest_power_level(min_size, max_size) == (
        total,
        coords,
        size,
    )


if __name__ == "__main__":
    with timeit("Building grid"):
        grid = Grid(serial_number=8199)
    with timeit("Part 1"):
        print(grid.square_with_largest_power_level())
    with timeit("Part 2"):
        print(grid.square_with_largest_power_level(min_size=1, max_size=300))
