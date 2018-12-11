#!/usr/bin/env python
"""
Using a deque with rotate() (fast!)

Based on https://www.reddit.com/r/adventofcode/comments/a4i97s/2018_day_9_solutions/ebepyc7
"""
import sys
import time
from collections import defaultdict, deque
from contextlib import contextmanager

import pytest


def parse(text):
    words = text.split()
    return int(words[0]), int(words[6])


class Marbles:
    def __init__(self, values, players=2):
        self.marbles = deque(values)
        self.players = players
        self.scores = defaultdict(int)

    def play_marbles_until(self, last_marble):
        for number in range(1, last_marble + 1):
            self.play_marble(number)

    def play_marble(self, number):
        if number % 23 != 0:
            self.marbles.rotate(-1)
            self.marbles.append(number)
        else:
            self.marbles.rotate(7)
            self.scores[number % self.players] += number + self.marbles.pop()
            self.marbles.rotate(-1)

    def high_score(self):
        return max(self.scores.values()) if self.scores else 0


@pytest.mark.parametrize("players, last_marble, high_score", [
    (9, 32, 32),
    (10, 1618, 8317),
    (13, 7999, 146373),
    (17, 1104, 2764),
    (21, 6111, 54718),
    (30, 5807, 37305),
])
def test_high_score(players, last_marble, high_score):
    marbles = Marbles([0], players=players)
    marbles.play_marbles_until(last_marble)
    assert marbles.high_score() == high_score


@contextmanager
def timeit(label):
    start = time.monotonic()
    yield
    end = time.monotonic()
    print(f"{label}: {end - start:.2}s")


def main():
    players, last_marble = parse(sys.stdin.read())

    # Part 1
    with timeit("Part 1"):
        marbles = Marbles([0], players=players)
        marbles.play_marbles_until(last_marble)
        print(marbles.high_score())

    # Part 2
    with timeit("Part 2"):
        marbles = Marbles([0], players=players)
        marbles.play_marbles_until(last_marble * 100)
        print(marbles.high_score())


if __name__ == '__main__':
    main()
