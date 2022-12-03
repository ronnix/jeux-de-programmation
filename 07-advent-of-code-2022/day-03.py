# https://adventofcode.com/2022/day/3

from functools import reduce
from operator import and_
from typing import Iterable, Set

from more_itertools import chunked, divide


EXAMPLE_INPUT = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


# === Part 1 ===


def test_part1():
    assert part1(EXAMPLE_INPUT) == 157


def part1(text: str) -> int:
    return sum(priority(common_item(divide(2, line))) for line in text.splitlines())


def common_item(strings: Iterable[str]) -> str:
    common = intersection(set(s) for s in strings)
    assert len(common) == 1
    return common.pop()


def intersection(sets: Iterable[Set]) -> Set:
    return reduce(and_, sets)


def priority(letter: str) -> int:
    return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".find(letter) + 1


# === Part 2 ===


def test_part2():
    assert part2(EXAMPLE_INPUT) == 70


def part2(text: str) -> int:
    return sum(priority(common_item(group)) for group in chunked(text.splitlines(), 3))


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    for line in text.splitlines():
        assert len(line) % 2 == 0
    print("Part 1:", part1(text))
    print("Part 2:", part2(text))
