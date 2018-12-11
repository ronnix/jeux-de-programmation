#!/usr/bin/env python
"""
Implement a circular linked list (even slower?)
"""
import sys
import time
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass

import pytest


def parse(text):
    words = text.split()
    return int(words[0]), int(words[6])


@pytest.mark.parametrize("marbles, current, number, new_marbles, new_current, high_score", [
    ([0], 0, 1, [0, 1], 1, 0),
    ([0, 1], 1, 2, [0, 2, 1], 1, 0),
    ([0, 2, 1], 1, 3, [0, 2, 1, 3], 3, 0),
    (
        [0, 16, 8, 17, 4, 18, 9, 19, 2, 20, 10, 21, 5, 11, 1, 12, 6, 13, 3, 14, 7, 15],
        11,
        22,
        [0, 16, 8, 17, 4, 18, 9, 19, 2, 20, 10, 21, 5, 22, 11, 1, 12, 6, 13, 3, 14, 7, 15],
        13,
        0,
    ),
    (
        [0, 16, 8, 17, 4, 18, 9, 19, 2, 20, 10, 21, 5, 22, 11, 1, 12, 6, 13, 3, 14, 7, 15],
        13,
        23,
        [0, 16, 8, 17, 4, 18, 19, 2, 20, 10, 21, 5, 22, 11, 1, 12, 6, 13, 3, 14, 7, 15],
        6,
        32,
    ),
])
def test_add_marble(marbles, current, number, new_marbles, new_current, high_score):
    m = Marbles(marbles, players=2, current=current)
    m.play_marble(number)
    assert list(m.marbles) == new_marbles
    assert m.current == new_current
    assert m.high_score() == high_score


class CircularList:

    @dataclass
    class Node:
        value: int
        prev: "Node"
        next: "Node"

    def __init__(self, values):
        values_iter = iter(values)
        value = next(values_iter)
        node = CircularList.Node(value=0, prev=None, next=None)
        self.first = node.prev = node.next = node
        self.size = 1
        for value in values_iter:
            node = CircularList.Node(value=value, prev=node, next=node.next)
            node.prev.next = node.next.prev = node
            self.size += 1

    def __iter__(self):
        node = self.first
        for _ in range(self.size):
            yield node.value
            node = node.next

    def insert_after(self, index, value):
        node = self.first
        for _ in range(index):
            node = node.next
        new_node = CircularList.Node(value=value, prev=node, next=node.next)
        node.next = new_node.next.prev = new_node
        self.size += 1

    def pop(self, index):
        node = self.first
        for _ in range(index):
            node = node.next
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        return node.value

    def __len__(self):
        return self.size


class Marbles:
    def __init__(self, values, players=2, current=0):
        self.marbles = CircularList(values)
        self.current = current
        self.players = players
        self.scores = defaultdict(int)

    def play_marbles_until(self, last_marble):
        for number in range(1, last_marble + 1):
            self.play_marble(number)

    def play_marble(self, number):
        if number % 23 != 0:
            previous = (self.current + 1) % len(self.marbles)
            self.marbles.insert_after(previous, number)
            self.current = (previous + 1) % len(self.marbles)
        else:
            player = number % self.players
            self.current = (self.current - 7) % len(self.marbles)
            self.scores[player] += number
            self.scores[player] += self.marbles.pop(self.current)

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
