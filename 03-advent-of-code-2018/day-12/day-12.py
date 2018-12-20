#!/usr/bin/env python
import time
from contextlib import contextmanager
from typing import NamedTuple, Tuple

import pytest
from tqdm import tqdm


@contextmanager
def timeit(label):
    start = time.monotonic()
    yield
    end = time.monotonic()
    print(f"{label}: {end - start:.2}s")


def test_initial_state():
    assert State.from_string("#..#.#..##......###...###") == {
        0,
        3,
        5,
        8,
        9,
        16,
        17,
        18,
        22,
        23,
        24,
    }


def test_rules():
    assert Rule.from_string("..#.# => #") == Rule((0, 0, 1, 0, 1), 1)


@pytest.mark.parametrize(
    "generations,result,total",
    [
        (1, {0, 4, 9, 15, 18, 21, 24}, 91),
        (
            20,
            {-2, 3, 4, 9, 10, 11, 12, 13, 17, 18, 19, 20, 21, 22, 23, 28, 30, 33, 34},
            325,
        ),
    ],
)
def test_next_state(generations, result, total):
    rules = [
        Rule.from_string(s)
        for s in [
            "...## => #",
            "..#.. => #",
            ".#... => #",
            ".#.#. => #",
            ".#.## => #",
            ".##.. => #",
            ".#### => #",
            "#.#.# => #",
            "#.### => #",
            "##.#. => #",
            "##.## => #",
            "###.. => #",
            "###.# => #",
            "####. => #",
        ]
    ]
    state = State.from_string("#..#.#..##......###...###")
    for _ in range(generations):
        state = state.apply(rules)
    assert state == result
    assert sum(state) == total


class State(set):
    @classmethod
    def from_string(cls, s):
        return cls(index for index, char in enumerate(s) if char == "#")

    def apply(self, rules):
        next_state = State()
        for pot in range(min(self) - 2, max(self) + 3):
            for rule in rules:
                if rule.matches(pot, self):
                    next_state.add(pot)
                    break
        return next_state


class Rule(NamedTuple):
    configuration: Tuple[int, int, int, int, int]
    result: int

    @classmethod
    def from_string(cls, s):
        return cls(
            configuration=tuple(1 if c == "#" else 0 for c in s[0:5]),
            result=1 if s[9] == "#" else 0,
        )

    def matches(self, pot, state):
        return all(
            (p not in state) ^ expected
            for p, expected in enumerate(self.configuration, start=pot - 2)
        )


def solve(generations):
    with open("input.txt") as input_file:
        state = State.from_string(input_file.readline().strip()[15:])
        rules = [
            Rule.from_string(line) for line in input_file if line.strip().endswith("#")
        ]

    for _ in tqdm(range(generations)):
        state = state.apply(rules)
    print(sum(state))


def main():
    with timeit("Part 1"):
        solve(20)

    with timeit("Part 2"):
        solve(50_000_000_000)


if __name__ == "__main__":
    main()
