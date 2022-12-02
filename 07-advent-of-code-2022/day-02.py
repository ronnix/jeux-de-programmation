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
    return sum(round_score(round) for round in text.splitlines())


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

OUTCOME = {
    ("Rock", "Scissors"): "win",
    ("Scissors", "Paper"): "win",
    ("Paper", "Rock"): "win",
    ("Rock", "Rock"): "draw",
    ("Paper", "Paper"): "draw",
    ("Scissors", "Scissors"): "draw",
    ("Scissors", "Rock"): "lose",
    ("Paper", "Scissors"): "lose",
    ("Rock", "Paper"): "lose",
}

OUTCOME_POINTS = {
    "lose": 0,
    "draw": 3,
    "win": 6,
}


def round_score(line):
    their_move, my_move = line.split()

    their_shape = THEIR_SHAPES[their_move]
    my_shape = MY_SHAPES[my_move]

    outcome = OUTCOME[(my_shape, their_shape)]

    shape_points = SHAPE_POINTS[my_shape]
    outcome_points = OUTCOME_POINTS[outcome]

    return shape_points + outcome_points


def read_puzzle_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
