from functools import reduce
from operator import or_
from textwrap import dedent


def make_groups(text):
    return [
        [make_bitvector(line.strip()) for line in chunk.splitlines()]
        for chunk in text.split("\n\n")
    ]


def make_bitvector(line):
    return sum(2 ** (ord(char) - ord("a")) for char in line)


def count_answers(groups):
    return sum(bin(reduce(or_, group)).count("1") for group in groups)


def test_make_groups():
    groups = make_groups(
        dedent(
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
    )
    assert len(groups) == 5
    assert len(groups[0]) == 1
    assert bin(groups[0][0]).count("1") == 3
    assert count_answers(groups) == 11


def part1(groups):
    return count_answers(groups)


if __name__ == "__main__":
    with open("day06.txt") as f:
        groups = make_groups(f.read())
    print("Part 1:", part1(groups))
