# https://adventofcode.com/2021/day/6

from typing import List


SAMPLE_INPUT = "3,4,3,1,2"


# === Part 1 ===


def test_parsing():
    assert parse(SAMPLE_INPUT) == [3, 4, 3, 1, 2]


def test_generations():
    states = parse(SAMPLE_INPUT)
    assert generations(states, 0) == [3, 4, 3, 1, 2]
    assert generations(states, 1) == [2, 3, 2, 0, 1]
    assert generations(states, 10) == [0, 1, 0, 5, 6, 0, 1, 2, 2, 3, 7, 8]


def generations(states: List[int], n: int) -> List[int]:
    for _ in range(n):
        states = next_generation(states)
    return states


def next_generation(states: List[int]) -> List[int]:
    older_fish = [6 if state == 0 else state - 1 for state in states]
    newborn_fish = [8 for state in states if state == 0]
    return older_fish + newborn_fish


def next_state(state: int) -> List[int]:
    if state > 0:
        return [state - 1]
    return [6, 8]


def test_part1():
    assert part1(parse(SAMPLE_INPUT)) == 5934


def part1(states) -> int:
    return len(generations(states, 80))


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> List[int]:
    return [int(s) for s in text.split(",")]


if __name__ == "__main__":
    states = parse(read_input())
    print("Part 1:", part1(states))
