# https://adventofcode.com/2022/day/3

from typing import List

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
    return sum(priority(common_item(line)) for line in text.splitlines())


def common_item(line: str) -> str:
    first, second = (set(half) for half in divide(2, line))
    common = first.intersection(second)
    assert len(common) == 1
    return common.pop()


def priority(letter: str) -> int:
    if "a" <= letter <= "z":
        return ord(letter) - 96
    if "A" <= letter <= "Z":
        return ord(letter) - 38
    raise ValueError


# === Part 2 ===


def test_part2():
    assert part2(EXAMPLE_INPUT) == 70


def part2(text: str) -> int:
    return sum(priority(badge_item(group)) for group in chunked(text.splitlines(), 3))


def badge_item(lines: List[str]) -> str:
    first, second, third = (set(line) for line in lines)
    common = first.intersection(second).intersection(third)
    assert len(common) == 1
    return common.pop()


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    for line in text.splitlines():
        assert len(line) % 2 == 0
    print("Part 1:", part1(text))
    print("Part 2:", part2(text))
