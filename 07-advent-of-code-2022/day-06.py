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
    return find_sequence_of_different_chars(text, 4)


def find_sequence_of_different_chars(text: str, length: int) -> int:
    for index, chars in enumerate(windowed(text, length)):
        if len(set(chars)) == length:
            return index + length
    raise KeyError


# === Part 2 ===


@pytest.mark.parametrize(
    "signal,result",
    [
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
        ("nppdvjthqldpwncqszvftbrmjlhg", 23),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
    ],
)
def test_part2(signal, result):
    assert part2(signal) == result


def part2(text: str) -> int:
    return find_sequence_of_different_chars(text, 14)


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
    print("Part 2:", part2(text))
