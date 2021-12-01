# https://adventofcode.com/2021/day/1

from itertools import pairwise


SAMPLE_INPUT = """\
199
200
208
210
200
207
240
269
260
263"""


def test_part1():
    assert part1(parse(SAMPLE_INPUT)) == 7


def part1(numbers):
    return sum(1 if b > a else 0 for a, b in pairwise(numbers))


def read_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text):
    return [int(line) for line in text.splitlines()]


if __name__ == "__main__":
    print("Part 1:", part1(parse(read_input())))
