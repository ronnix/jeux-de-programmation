# https://adventofcode.com/2023/day/4
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Set
import re

import pytest


EXAMPLE_CARDS = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def test_part1():
    assert part1(EXAMPLE_CARDS) == 13


def part1(text: str) -> int:
    cards = [Card.from_string(line) for line in text.splitlines() if line]
    return sum(card.points() for card in cards)


def test_parse_card():
    card = Card.from_string("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    assert card.winning_numbers == {41, 48, 83, 86, 17}
    assert card.numbers_you_have == {83, 86, 6, 31, 17, 9, 48, 53}
    assert card.points


def test_card_points():
    cards = [Card.from_string(line) for line in EXAMPLE_CARDS.splitlines() if line]
    assert [card.points() for card in cards] == [8, 2, 2, 1, 0, 0]


@dataclass
class Card:
    winning_numbers: Set[int]
    numbers_you_have: Set[int]

    @classmethod
    def from_string(cls, text: str) -> Card:
        identification, numbers = text.split(":")
        winning_numbers, numbers_you_have = numbers.split("|")
        return cls(
            winning_numbers={int(n) for n in re.split(r"\s+", winning_numbers.strip())},
            numbers_you_have={
                int(n) for n in re.split(r"\s+", numbers_you_have.strip())
            },
        )

    def points(self):
        nb_winning = len(self.numbers_you_have.intersection(self.winning_numbers))
        if nb_winning > 0:
            return 2 ** (nb_winning - 1)
        return 0


if __name__ == "__main__":
    puzzle_input = Path("day04.txt").read_text()
    print("Part 1", part1(puzzle_input))
