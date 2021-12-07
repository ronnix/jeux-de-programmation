# https://adventofcode.com/2021/day/7

from typing import List


SAMPLE_INPUT = "16,1,2,0,4,2,7,1,2,14"


# === Part 1 ===


def test_parsing():
    assert parse(SAMPLE_INPUT) == [16,1,2,0,4,2,7,1,2,14]


def test_part1():
    assert part1(parse(SAMPLE_INPUT)) == 37


def part1(xs: List[int]) -> int:
    return min_required_fuel(xs)


def min_required_fuel(xs: List[int]) -> int:
    min_x = min(xs)
    max_x = max(xs)
    return min(required_fuel(xs, x) for x in range(min_x, max_x + 1))


def required_fuel(xs: List[int], target_x: int):
    return sum(abs(x - target_x) for x in xs)


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> List[int]:
    return [int(s) for s in text.split(",")]


if __name__ == "__main__":
    xs = parse(read_input())
    print("Part 1:", part1(xs))
