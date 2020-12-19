from functools import reduce
from operator import and_, or_
from textwrap import dedent

import pytest


@pytest.fixture
def sample_input():
    return dedent(
        """\
            abc

            a
            b
            c

            ab
            ac

            a
            a
            a
            a

            b
            """
    )


@pytest.fixture
def sample_groups(sample_input):
    return make_groups(sample_input)


def make_groups(text):
    return [
        [make_bitvector(line.strip()) for line in chunk.splitlines()]
        for chunk in text.split("\n\n")
    ]


def make_bitvector(line):
    return sum(2 ** (ord(char) - ord("a")) for char in line)


def count_answers_any(groups):
    return sum(popcount(reduce(or_, group)) for group in groups)


def popcount(number):
    return bin(number).count("1")


def test_count_answers_any(sample_groups):
    assert count_answers_any(sample_groups) == 11


def test_count_answers_all(sample_groups):
    assert count_answers_all(sample_groups) == 6


def count_answers_all(groups):
    return sum(popcount(reduce(and_, group)) for group in groups)


def part1(groups):
    return count_answers_any(groups)


def part2(groups):
    return count_answers_all(groups)


if __name__ == "__main__":
    with open("day06.txt") as f:
        groups = make_groups(f.read())
    print("Part 1:", part1(groups))
    print("Part 2:", part2(groups))
