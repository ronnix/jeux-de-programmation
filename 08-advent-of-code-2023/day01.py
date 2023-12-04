# https://adventofcode.com/2023/day/1

from pathlib import Path
from textwrap import dedent

import pytest


EXAMPLE_INPUT = dedent(
    """
    1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet
    """
)


@pytest.mark.parametrize(
    "line, value",
    [
        ("1abc2", 12),
        ("pqr3stu8vwx", 38),
        ("a1b2c3d4e5f", 15),
        ("treb7uchet", 77),
    ],
)
def test_calibration_value(line, value):
    assert calibration_value(line) == value


def calibration_value(line):
    digits = [char for char in line if char.isdigit()]
    first = digits[0]
    last = digits[-1]
    return int(first + last)


def test_part1():
    assert part1(EXAMPLE_INPUT) == 142


def part1(text):
    return sum(calibration_value(line) for line in text.splitlines() if line)


if __name__ == "__main__":
    print("Part 1", part1(Path("day01.txt").read_text()))
