#!/usr/bin/env python
from functools import lru_cache
import pytest


SERIAL_NUMBER = 8199


@pytest.mark.parametrize("coords, serial_number, result", [
    ((3, 5), 8, 4),
    ((122, 79), 57, -5),
    ((217, 196), 39, 0),
    ((101, 153), 71, 4),
])
def test_cell_power_level(coords, serial_number, result):
    assert cell_power_level(coords, serial_number) == result


@lru_cache(maxsize=None)
def cell_power_level(coords=None, serial_number=None):
    x, y = coords
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    hundreds_digit = power_level // 100 % 10
    return hundreds_digit - 5


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
    assert square_with_largest_power_level(serial_number, min_size, max_size) == (
        total,
        coords,
        size,
    )


def square_with_largest_power_level(serial_number, min_size=3, max_size=3):
    return max(
        (square_power_level((x, y), serial_number, size), (x, y), size)
        for size in range(min_size, max_size + 1)
        for x in range(1, 300 - size + 1)
        for y in range(1, 300 - size + 1)
    )


@lru_cache(maxsize=None)
def square_power_level(coords, serial_number, size):
    if size == 1:
        return cell_power_level(coords, serial_number)
    x, y = coords
    x_right = x + size - 1
    y_bottom = y + size - 1
    return (
        square_power_level(coords, serial_number, size - 1)
        + sum(cell_power_level((x + dx, y_bottom), serial_number) for dx in range(size))
        + sum(
            cell_power_level((x_right, y + dy), serial_number) for dy in range(size - 1)
        )
    )


if __name__ == "__main__":
    print(square_with_largest_power_level(8199))
    print(square_with_largest_power_level(8199, min_size=1, max_size=300))
