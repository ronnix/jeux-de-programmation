#!/usr/bin/env python
import sys

import pytest


@pytest.mark.parametrize("unit1, unit2, res", [
    ("r", "R", True),
    ("R", "r", True),
    ("r", "s", False),
    ("a", "a", False),
    ("A", "A", False),
])
def test_units_react(unit1, unit2, res):
    assert units_react(unit1, unit2) is res


def units_react(unit1, unit2):
    return abs(ord(unit1) - ord(unit2)) == 32


@pytest.mark.parametrize("input, output", [
    ("Aa", ""),
    ("abBA", ""),
    ("abAB", "abAB"),
    ("aabAAB", "aabAAB"),
    ("dabAcCaCBAcCcaDA", "dabCBAcaDA"),
])
def test_reduce_polymer(input, output):
    assert reduce_polymer(input) == output


def reduce_polymer(units):
    index = 0
    while index < len(units) - 1:
        if units_react(units[index], units[index + 1]):
            units = units[:index] + units[index + 2:]
            index = max(0, index - 1)
            continue
        index += 1
    return "".join(units)


def main():
    print(len(reduce_polymer(sys.stdin.read())))


if __name__ == '__main__':
    main()
