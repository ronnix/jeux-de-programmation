from itertools import combinations
from textwrap import dedent

import pytest


@pytest.fixture
def sample_input():
    return parse_input(
        dedent(
            """\
            35
            20
            15
            25
            47
            40
            62
            55
            65
            95
            102
            117
            150
            182
            127
            219
            299
            277
            309
            576
            """
        )
    )


def parse_input(text):
    return [int(line) for line in text.splitlines()]


def test_first_invalid_number(sample_input):
    assert first_invalid_number(sample_input, 5) == 127


def first_invalid_number(numbers, size):
    for i, n in enumerate(numbers[size:]):
        if not any(n == sum(pair) for pair in combinations(numbers[i : i + size], 2)):
            return n


def part1(numbers):
    return first_invalid_number(numbers, 25)


if __name__ == "__main__":
    with open("day09.txt") as f:
        numbers = parse_input(f.read())
    print("Part 1:", part1(numbers))
