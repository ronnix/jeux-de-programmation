# https://adventofcode.com/2021/day/13

from typing import List, Set, Tuple


SAMPLE_INPUT = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


# === Part 1 ===

Point = Tuple[int, int]
Axis = str
Fold = Tuple[Axis, int]


def test_parsing() -> None:
    dots, folds = parse(SAMPLE_INPUT)
    assert len(dots) == 18
    assert dots[2] == (9, 10)
    assert len(folds) == 2
    assert folds[0] == ("y", 7)


def test_fold() -> None:
    before, _ = parse(SAMPLE_INPUT)
    print(as_string(set(before)))

    after_first = fold_horizontally(set(before), 7)
    print(as_string(set(after_first)))
    assert len(after_first) == 17

    after_second = fold_vertically(set(after_first), 5)
    print(as_string(set(after_second)))
    assert len(after_second) == 16


def as_string(dots: Set[Point]) -> str:
    res = "\n"
    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in dots:
                res += "#"
            else:
                res += "."
        res += "\n"
    return res


def fold(dots: Set[Point], folds: List[Fold]) -> Set[Point]:
    for (axis, line) in folds:
        if axis == "y":
            dots = fold_horizontally(dots, line)
        elif axis == "x":
            dots = fold_vertically(dots, line)
        else:
            raise ValueError
    return dots


def fold_horizontally(dots: Set[Point], fold_line: int) -> Set[Point]:
    return {(x, y) if y < fold_line else (x, 2 * fold_line - y) for x, y in dots}


def fold_vertically(dots: Set[Point], fold_line: int) -> Set[Point]:
    return {(x, y) if x < fold_line else (2 * fold_line - x, y) for x, y in dots}


def test_part1() -> None:
    assert part1(*parse(SAMPLE_INPUT)) == 17


def part1(dots: List[Point], folds: List[Fold]) -> int:
    return len(fold(set(dots), folds[:1]))


# === Part 2 ===


def part2(dots: List[Point], folds: List[Fold]) -> str:
    return as_string(fold(set(dots), folds))


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> Tuple[List[Point], List[Fold]]:
    dot_lines, fold_lines = text.split("\n\n", 1)
    dots = [parse_point(line) for line in dot_lines.splitlines()]
    folds = [parse_fold(line) for line in fold_lines.splitlines()]
    return dots, folds


def parse_point(line: str) -> Point:
    x, y = line.split(",", 1)
    return int(x), int(y)


def parse_fold(line: str) -> Fold:
    axis, value = line.split(" ")[2].split("=")
    assert axis in {"x", "y"}
    return axis, int(value)


if __name__ == "__main__":
    print("Part 1:", part1(*parse(read_input())))
    print("Part 2:", part2(*parse(read_input())))
