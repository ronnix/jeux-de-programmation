# https://adventofcode.com/2021/day/2


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
    return [sum(x) for x in zip(*(movement(*step) for step in steps))]


def movement(command, amount):
    if command == "forward":
        return (amount, 0)
    if command == "down":
        return (0, amount)
    if command == "up":
        return (0, -amount)
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
