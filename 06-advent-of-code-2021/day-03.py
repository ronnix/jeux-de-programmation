# https://adventofcode.com/2021/day/3

from statistics import mean

SAMPLE_INPUT = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


# === Part 1 ===


def test_part1():
    assert part1(parse(SAMPLE_INPUT)) == 198


def part1(numbers):
    gamma_rate_digits = most_common_bits(numbers)
    epsilon_rate_digits = reverse_bits(gamma_rate_digits)
    return to_number(gamma_rate_digits) * to_number(epsilon_rate_digits)


def most_common_bits(numbers):
    return [round(mean(column)) for column in zip(*numbers)]


def to_number(digits):
    return int("".join(map(str, digits)), 2)


def reverse_bits(digits):
    return [int(not digit) for digit in digits]


# === Input parsing ===


def read_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text):
    return [parse_line(line) for line in text.splitlines()]


def parse_line(line):
    return [int(char) for char in line]


if __name__ == "__main__":
    numbers = parse(read_input())
    print("Part 1:", part1(numbers))
