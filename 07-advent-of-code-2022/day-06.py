# https://adventofcode.com/2022/day/6

from more_itertools import windowed

import pytest


# === Part 1 ===


@pytest.mark.parametrize(
    "signal,result",
    [
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
        ("nppdvjthqldpwncqszvftbrmjlhg", 6),
    ],
)
def test_part1(signal, result):
    assert part1(signal) == result


def part1(text: str) -> int:
    for index, chars in enumerate(windowed(text, 4)):
        if len(set(chars)) == 4:
            return index + 4
    raise RuntimeError


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
