# https://adventofcode.com/2022/day/2

from enum import Enum


EXAMPLE_INPUT = """\
A Y
B X
C Z
"""


# === Part 1 ===


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6


def test_part1():
    assert part1(EXAMPLE_INPUT) == 15


def part1(text):
    return sum(line_score_part1(line) for line in text.splitlines())


THEIR_SHAPES = {
    "A": Shape.ROCK,
    "B": Shape.PAPER,
    "C": Shape.SCISSORS,
}

MY_SHAPES = {
    "X": Shape.ROCK,
    "Y": Shape.PAPER,
    "Z": Shape.SCISSORS,
}

BEATS = {
    Shape.ROCK: Shape.SCISSORS,
    Shape.SCISSORS: Shape.PAPER,
    Shape.PAPER: Shape.ROCK,
}

LOSES_TO = {value: key for key, value in BEATS.items()}


def line_score_part1(line):
    their_move, my_move = line.split()
    return round_score(THEIR_SHAPES[their_move], MY_SHAPES[my_move])


def round_score(their_shape, my_shape):
    return my_shape.value + outcome(my_shape, their_shape).value


def outcome(my_shape, their_shape):
    if BEATS[my_shape] == their_shape:
        return Outcome.WIN
    if BEATS[their_shape] == my_shape:
        return Outcome.LOSE
    return Outcome.DRAW


# === Part 2 ===


def test_part2():
    assert part2(EXAMPLE_INPUT) == 12


def part2(text):
    return sum(line_score_part2(line) for line in text.splitlines())


def line_score_part2(line):
    their_move, desired_outcome = line.split()
    their_shape = THEIR_SHAPES[their_move]
    my_shape = shape_to_play(their_shape, desired_outcome)
    return round_score(their_shape, my_shape)


def shape_to_play(their_shape, desired_outcome):
    if desired_outcome == "X":  # lose
        return BEATS[their_shape]
    if desired_outcome == "Y":  # draw
        return their_shape
    if desired_outcome == "Z":  # win
        return LOSES_TO[their_shape]


def read_puzzle_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
    print("Part 2:", part2(text))
