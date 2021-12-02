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


def test_part2():
    assert part2(parse(SAMPLE_INPUT)) == 900


def part2(steps):
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
    print("Part 2:", part2(steps))
