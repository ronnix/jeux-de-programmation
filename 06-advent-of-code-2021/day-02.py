# https://adventofcode.com/2021/day/2

from functools import reduce

SAMPLE_INPUT = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2"""


def test_part1():
    assert part1(parse(SAMPLE_INPUT)) == 150


def part1(steps):
    x, y = integrate_movements(steps)
    return x * y


def integrate_movements(steps):
    return sum_vectors(movement(*step) for step in steps)


def sum_vectors(vectors):
    return [sum(x) for x in zip(*vectors)]


def movement(command, amount):
    if command == "forward":
        return (amount, 0)
    if command == "down":
        return (0, amount)
    if command == "up":
        return (0, -amount)
    raise ValueError


def test_part2_imperative():
    assert part2_imperative(parse(SAMPLE_INPUT)) == 900


def part2_imperative(steps):
    x, y = integrate_movements_with_aim(steps)
    return x * y


def integrate_movements_with_aim(steps):
    x, y, aim = 0, 0, 0
    for step in steps:
        dx, dy, daim = movement_with_aim(*step, aim)
        aim += daim
        x += dx
        y += dy
    return x, y


def movement_with_aim(command, amount, aim):
    if command == "forward":
        return (amount, aim * amount, 0)
    if command == "down":
        return (0, 0, amount)
    if command == "up":
        return (0, 0, -amount)
    raise ValueError


def test_part2_functional():
    assert part2_functional(parse(SAMPLE_INPUT)) == 900


def part2_functional(steps):
    x, y, aim = foldl(next_state, (0, 0, 0), steps)
    return x * y


def foldl(function, initializer, iterable):  # Haskell-like fold left
    return reduce(function, iterable, initializer)


def next_state(state, step):
    x, y, aim = state
    command, amount = step
    if command == "forward":
        return (x + amount, y + aim * amount, aim)
    if command == "down":
        return (x, y, aim + amount)
    if command == "up":
        return (x, y, aim - amount)
    raise ValueError


def read_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text):
    return [parse_line(line) for line in text.splitlines()]


def parse_line(line):
    command, amount = line.split(" ")
    return command, int(amount)


if __name__ == "__main__":
    steps = parse(read_input())
    print("Part 1:", part1(steps))
    print("Part 2 (imperative):", part2_imperative(steps))
    print("Part 2 (functional):", part2_functional(steps))
