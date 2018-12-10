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
    m = Marbles(marbles, current=current)
    m.add(number)
    assert m == new_marbles
    assert m.current == new_current


class Marbles(list):
    def __init__(self, args, current=0):
        super().__init__(args)
        self.current = current

    def add(self, number):
        self.current = (self.current + 2) % len(self)
        if self.current == 0:
            self.current = len(self)
            self.append(number)
        else:
            self.insert(self.current, number)


def main():
    players, points = parse(sys.stdin.read())
    print(players, points)


if __name__ == '__main__':
    main()
