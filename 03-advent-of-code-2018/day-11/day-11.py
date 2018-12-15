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
