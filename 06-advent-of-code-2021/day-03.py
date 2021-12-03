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
    return [round_digit_up(mean(column)) for column in zip(*numbers)]


def to_number(digits):
    return int("".join(map(str, digits)), 2)


def reverse_bits(digits):
    return [int(not digit) for digit in digits]


def round_digit_up(value):
    if 0 <= value < 0.5:
        return 0
    elif 0.5 <= value <= 1:
        return 1
    else:
        raise ValueError


# === Part 2 ===


def test_part2():
    numbers = parse(SAMPLE_INPUT)
    assert find_oxygen_generator_rating(numbers) == 23
    assert find_co2_scrubber_rating(numbers) == 10
    assert part2(numbers) == 230


def part2(numbers):
    oxygen_generator_rating = find_oxygen_generator_rating(numbers)
    co2_scrubber_rating = find_co2_scrubber_rating(numbers)
    return oxygen_generator_rating * co2_scrubber_rating

def find_oxygen_generator_rating(numbers):
    return to_number(filter_numbers(numbers, func=most_common_bits))


def find_co2_scrubber_rating(numbers):
    return to_number(filter_numbers(numbers, func=least_common_bits))


def least_common_bits(numbers):
    return reverse_bits(most_common_bits(numbers))


def filter_numbers(numbers, func, index=0):
    criteria = func(numbers)
    filtered = [number for number in numbers if number[index] == criteria[index]]
    if len(filtered) == 1:
        return filtered[0]
    return filter_numbers(filtered, func=func, index=index + 1)


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
    print("Part 2:", part2(numbers))
