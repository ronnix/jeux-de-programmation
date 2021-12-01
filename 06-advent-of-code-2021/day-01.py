# https://adventofcode.com/2021/day/1

try:
    from itertools import pairwise  # Python ≥ 3.10
except:
    from more_itertools import pairwise

from more_itertools import windowed


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


def test_part2():
    assert part2(parse(SAMPLE_INPUT)) == 5


def part2(numbers):
    sums = (sum(triplet) for triplet in windowed(numbers, 3))
    return sum(1 if b > a else 0 for a, b in pairwise(sums))


def read_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text):
    return [int(line) for line in text.splitlines()]


if __name__ == "__main__":
    print("Part 1:", part1(parse(read_input())))
    print("Part 2:", part2(parse(read_input())))
