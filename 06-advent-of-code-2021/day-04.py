# https://adventofcode.com/2021/day/4

import re
from dataclasses import dataclass, field
from typing import List, Set, Tuple

from more_itertools import chunked


SAMPLE_INPUT = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


# === Part 1 ===


def test_parsing():
    numbers, boards = parse(SAMPLE_INPUT)
    assert len(numbers) == 27
    assert len(boards) == 3
    assert boards[0].lines()[0] == [22, 13,17, 11, 0]
    assert boards[0].columns()[0] == [22, 8,21, 6, 1]


def test_play():
    numbers, boards = parse(SAMPLE_INPUT)
    last_number_called, winning_board = play(numbers, boards)
    assert last_number_called == 24
    assert sum(winning_board.unmarked_numbers()) == 188


def test_part1():
    numbers, boards = parse(SAMPLE_INPUT)
    assert part1(numbers, boards) == 4512


def part1(numbers, boards):
    last_number_called, winning_board = play(numbers, boards)
    return last_number_called * sum(winning_board.unmarked_numbers())


@dataclass
class Board:
    numbers: List[int]
    marked: Set[int] = field(default_factory=set)

    def mark(self, number: int):
        if number in self.numbers:
            self.marked.add(number)

    def wins(self):
        return self.line_filled() or self.column_filled()

    def line_filled(self):
        return any(all(number in self.marked for number in line) for line in self.lines())

    def column_filled(self):
        return any(all(number in self.marked for number in column) for column in self.columns())

    def lines(self):
        return list(chunked(self.numbers, 5))

    def columns(self):
        return [[self.numbers[i+j] for i in range(0, 25, 5)] for j in range(5)]

    def unmarked_numbers(self):
        return [number for number in self.numbers if number not in self.marked]


def play(numbers, boards) -> Tuple[int, Board]:
    for number in numbers:
        for board in boards:
            board.mark(number)
            if board.wins():
                return number, board
    raise RuntimeError  # nobody wins


# === Input parsing ===


def read_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> Tuple[List[int], List[Board]]:
    chunks = text.split("\n\n")
    numbers = [int(number) for number in chunks[0].split(",")]
    boards = [parse_board(chunk) for chunk in chunks[1:]]
    return numbers, boards


def parse_board(chunk: str) -> Board:
    return Board(numbers=[int(number) for number in re.split(r"\s+", chunk) if number])


if __name__ == "__main__":
    numbers, boards = parse(read_input())
    print("Part 1:", part1(numbers, boards))
