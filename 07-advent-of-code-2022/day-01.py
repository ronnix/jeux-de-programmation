# https://adventofcode.com/2022/day/1

from more_itertools import split_at


EXAMPLE_INPUT = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


# === Part 1 ===


def test_part1():
    assert part1(EXAMPLE_INPUT) == 24000


def part1(text):
    lines = text.splitlines()
    return max(
        sum(int(line) for line in paragraph)
        for paragraph in split_at(lines, lambda line: line == "")
    )


def read_puzzle_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
