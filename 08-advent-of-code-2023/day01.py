# https://adventofcode.com/2023/day/1

from pathlib import Path
from textwrap import dedent
import re

import pytest


@pytest.mark.parametrize(
    "line, value, with_letters",
    [
        ("1abc2", 12, False),
        ("pqr3stu8vwx", 38, False),
        ("a1b2c3d4e5f", 15, False),
        ("treb7uchet", 77, False),
        ("two1nine", 29, True),
        ("eightwothree", 83, True),
        ("abcone2threexyz", 13, True),
        ("xtwone3four", 24, True),
        ("4nineeightseven2", 42, True),
        ("zoneight234", 14, True),
        ("7pqrstsixteen", 76, True),
    ],
)
def test_calibration_value(line, value, with_letters):
    assert calibration_value(line, with_letters) == value


DIGITS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def calibration_value(line, with_letters=False):
    patterns = [r"\d"]
    if with_letters:
        patterns.extend(DIGITS)
    digits = [
        int(match) if match.isdigit() else DIGITS.index(match)
        for match in overlapping_matches(patterns, line)
    ]
    first = digits[0]
    last = digits[-1]
    return (first * 10) + last


# The standard library's re.findall() returns non-overlapping matches,
# which does not give the correct result in a few cases. We could use
# the third-party `regex` library instead, which adds an option for
# overlapping matches. Or if we stick to the stdlib, we can use a
# capturing group inside a lookahead.
# https://stackoverflow.com/questions/5616822/how-to-use-regex-to-find-all-overlapping-matches
def overlapping_matches(patterns, text):
    regex = f"(?=({'|'.join(patterns)}))"
    return re.findall(regex, text)


def test_part1():
    assert (
        part1(
            dedent(
                """
                1abc2
                pqr3stu8vwx
                a1b2c3d4e5f
                treb7uchet
                """
            )
        )
        == 142
    )


def part1(text):
    return sum(calibration_value(line) for line in text.splitlines() if line)


def test_part2():
    assert (
        part2(
            dedent(
                """
                two1nine
                eightwothree
                abcone2threexyz
                xtwone3four
                4nineeightseven2
                zoneight234
                7pqrstsixteen
                """
            )
        )
        == 281
    )


def part2(text):
    return sum(
        calibration_value(line, with_letters=True) for line in text.splitlines() if line
    )


if __name__ == "__main__":
    print("Part 1", part1(Path("day01.txt").read_text()))
    print("Part 2", part2(Path("day01.txt").read_text()))
