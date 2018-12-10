#!/usr/bin/env python
import sys

import pytest


def test_parse():
    assert parse("426 players; last marble is worth 72058 points") == (426, 72058)


def parse(text):
    words = text.split()
    return int(words[0]), int(words[6])


@pytest.mark.parametrize("marbles, current, number, new_marbles, new_current", [
    ([0], 0, 1, [0, 1], 1),
    ([0, 1], 1, 2, [0, 2, 1], 1),
    ([0, 2, 1], 1, 3, [0, 2, 1, 3], 3),
    (
        [0, 16, 8, 17, 4, 18, 9, 19, 2, 20, 10, 21, 5, 11, 1, 12, 6, 13, 3, 14, 7, 15],
        11,
        22,
        [0, 16, 8, 17, 4, 18, 9, 19, 2, 20, 10, 21, 5, 22, 11, 1, 12, 6, 13, 3, 14, 7, 15],
        13,
    ),

])
def test_add_marble(marbles, current, number, new_marbles, new_current):
    assert add_marble(marbles, current, number) == (new_marbles, new_current)


def add_marble(marbles, current, number):
    new_marbles = marbles.copy()
    new_current = (current + 2) % len(marbles)
    if new_current == 0:
        new_current = len(marbles)
        new_marbles.append(number)
    else:
        new_marbles.insert(new_current, number)
    return new_marbles, new_current


def main():
    players, points = parse(sys.stdin.read())
    print(players, points)


if __name__ == '__main__':
    main()
