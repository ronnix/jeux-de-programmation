# https://adventofcode.com/2023/day/7
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
from typing import List

import pytest


EXAMPLE_HANDS = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def test_parse_hands():
    hands = Hand.parse_list(EXAMPLE_HANDS)
    assert hands == [
        Hand(cards="32T3K", bid=765),
        Hand(cards="T55J5", bid=684),
        Hand(cards="KK677", bid=28),
        Hand(cards="KTJJT", bid=220),
        Hand(cards="QQQJA", bid=483),
    ]


class HandType(IntEnum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


@pytest.mark.parametrize(
    "cards, hand_type",
    [
        ("AAAAA", HandType.FIVE_OF_A_KIND),
        ("AA8AA", HandType.FOUR_OF_A_KIND),
        ("23332", HandType.FULL_HOUSE),
        ("TTT98", HandType.THREE_OF_A_KIND),
        ("23432", HandType.TWO_PAIR),
        ("A23A4", HandType.ONE_PAIR),
        ("23456", HandType.HIGH_CARD),
    ],
)
def test_hand_type(cards, hand_type):
    assert Hand(cards, 1).hand_type == hand_type


def test_ranks():
    hands = Hand.parse_list(EXAMPLE_HANDS)
    ranks = [(hand.cards, rank) for rank, hand in enumerate(sorted(hands), 1)]
    assert ranks == [
        ("32T3K", 1),
        ("KTJJT", 2),
        ("KK677", 3),
        ("T55J5", 4),
        ("QQQJA", 5),
    ]


@dataclass(frozen=True)
class Hand:
    cards: str
    bid: int

    CARDS = "23456789TJQKA"  # by order of strength

    @classmethod
    def parse(cls, text: str) -> Hand:
        cards, bid = text.split(" ")
        return cls(cards=cards, bid=int(bid))

    @classmethod
    def parse_list(cls, text: str) -> List[Hand]:
        return [cls.parse(line) for line in text.splitlines() if line]

    @property
    def hand_type(self) -> HandType:
        counts = [count for _, count in Counter(self.cards).most_common()]
        if counts == [5]:
            return HandType.FIVE_OF_A_KIND
        elif counts == [4, 1]:
            return HandType.FOUR_OF_A_KIND
        elif counts == [3, 2]:
            return HandType.FULL_HOUSE
        elif counts == [3, 1, 1]:
            return HandType.THREE_OF_A_KIND
        elif counts == [2, 2, 1]:
            return HandType.TWO_PAIR
        elif counts == [2, 1, 1, 1]:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    def __lt__(self, other) -> bool:
        if self.hand_type == other.hand_type:
            for card, other_card in zip(self.cards, other.cards):
                if card != other_card:
                    return self.CARDS.index(card) < self.CARDS.index(other_card)
        return self.hand_type < other.hand_type


def test_part1():
    assert part1(EXAMPLE_HANDS) == 6440


def part1(text: str) -> int:
    hands = Hand.parse_list(text)
    total_winnings = sum(hand.bid * rank for rank, hand in enumerate(sorted(hands), 1))
    return total_winnings


@pytest.mark.parametrize(
    "cards, hand_type",
    [
        ("55555", HandType.FIVE_OF_A_KIND),
        ("5555J", HandType.FIVE_OF_A_KIND),
        ("555JJ", HandType.FIVE_OF_A_KIND),
        ("5JJJJ", HandType.FIVE_OF_A_KIND),
        ("JJJJJ", HandType.FIVE_OF_A_KIND),
        ("T5555", HandType.FOUR_OF_A_KIND),
        ("T555J", HandType.FOUR_OF_A_KIND),
        ("T55JJ", HandType.FOUR_OF_A_KIND),
        ("T55J5", HandType.FOUR_OF_A_KIND),
        ("T5JJJ", HandType.FOUR_OF_A_KIND),
        ("22333", HandType.FULL_HOUSE),
        ("2233J", HandType.FULL_HOUSE),
        ("23444", HandType.THREE_OF_A_KIND),
        ("2344J", HandType.THREE_OF_A_KIND),
        ("234JJ", HandType.THREE_OF_A_KIND),
        ("KK677", HandType.TWO_PAIR),
        ("32T3K", HandType.ONE_PAIR),
    ],
)
def test_hand_type_with_jokers(cards, hand_type):
    assert HandWithJoker(cards, 1).hand_type == hand_type


def test_ranks_with_jokers():
    hands = HandWithJoker.parse_list(EXAMPLE_HANDS)
    ranks = [
        (hand.cards, hand.hand_type, rank) for rank, hand in enumerate(sorted(hands), 1)
    ]
    assert ranks == [
        ("32T3K", HandType.ONE_PAIR, 1),
        ("KK677", HandType.TWO_PAIR, 2),
        ("T55J5", HandType.FOUR_OF_A_KIND, 3),
        ("QQQJA", HandType.FOUR_OF_A_KIND, 4),
        ("KTJJT", HandType.FOUR_OF_A_KIND, 5),
    ]


class HandWithJoker(Hand):
    CARDS = "J23456789TQKA"  # by order of strength

    @property
    def hand_type(self) -> HandType:
        counter = Counter(self.cards)
        nb_jokers = counter.pop("J", 0)
        counts = [count for _, count in counter.most_common()]
        if counts == [5 - nb_jokers] or nb_jokers == 5:
            return HandType.FIVE_OF_A_KIND
        elif counts == [4 - nb_jokers, 1]:
            return HandType.FOUR_OF_A_KIND
        elif counts == [3 - nb_jokers, 2]:
            return HandType.FULL_HOUSE
        elif counts == [3 - nb_jokers, 1, 1]:
            return HandType.THREE_OF_A_KIND
        elif counts == [2, 2, 1]:
            return HandType.TWO_PAIR
        elif counts == [2 - nb_jokers, 1, 1, 1]:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD


def test_part2():
    assert part2(EXAMPLE_HANDS) == 5905


def part2(text: str) -> int:
    hands = HandWithJoker.parse_list(text)
    total_winnings = sum(hand.bid * rank for rank, hand in enumerate(sorted(hands), 1))
    return total_winnings


def read_puzzle_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
    print("Part 2", part2(puzzle_input))
