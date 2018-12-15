#!/usr/bin/env python
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


def cell_power_level(coords=None, serial_number=None):
    x, y = coords
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    hundreds_digit = power_level // 100 % 10
    return hundreds_digit - 5


@pytest.mark.parametrize("serial_number, coords, total", [
    (18, (33, 45), 29),
    (42, (21, 61), 30),
])
def test_square_with_largest_power_level(serial_number, coords, total):
    assert square_with_largest_power_level(serial_number) == (total, coords)


def square_with_largest_power_level(serial_number):
    return max(
        (square_power_level((x, y), serial_number), (x, y))
        for x in range(1, 298)
        for y in range(1, 298)
    )


def square_power_level(coords, serial_number):
    x, y = coords
    return sum(
        cell_power_level((x + dx, y + dy), serial_number)
        for dx in range(3)
        for dy in range(3)
    )


if __name__ == '__main__':
    print(square_with_largest_power_level(8199))
