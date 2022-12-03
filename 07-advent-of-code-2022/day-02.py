# https://adventofcode.com/2022/day/2

EXAMPLE_INPUT = """\
A Y
B X
C Z
"""


# === Part 1 ===


def test_part1():
    assert part1(EXAMPLE_INPUT) == 15


def part1(text):
    return sum(line_score_part1(line) for line in text.splitlines())


THEIR_SHAPES = {
    "A": "Rock",
    "B": "Paper",
    "C": "Scissors",
}

MY_SHAPES = {
    "X": "Rock",
    "Y": "Paper",
    "Z": "Scissors",
}

SHAPE_POINTS = {
    "Rock": 1,
    "Paper": 2,
    "Scissors": 3,
}

BEATS = {
    "Rock": "Scissors",
    "Scissors": "Paper",
    "Paper": "Rock",
}

LOSES_TO = {value: key for key, value in BEATS.items()}

OUTCOME_POINTS = {
    "lose": 0,
    "draw": 3,
    "win": 6,
}


def line_score_part1(line):
    their_move, my_move = line.split()
    return round_score(THEIR_SHAPES[their_move], MY_SHAPES[my_move])


def round_score(their_shape, my_shape):
    shape_points = SHAPE_POINTS[my_shape]
    outcome_points = OUTCOME_POINTS[outcome(my_shape, their_shape)]

    return shape_points + outcome_points


def outcome(my_shape, their_shape):
    if BEATS[my_shape] == their_shape:
        return "win"
    if BEATS[their_shape] == my_shape:
        return "lose"
    return "draw"


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
