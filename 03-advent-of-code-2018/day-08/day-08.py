#!/usr/bin/env python
import sys


TEST_INPUT = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


def test_parse_input():
    assert parse_input(TEST_INPUT) == [
        2,
        3,
        0,
        3,
        10,
        11,
        12,
        1,
        1,
        0,
        1,
        99,
        2,
        1,
        1,
        2,
    ]


def parse_input(text):
    return [int(s) for s in text.split()]


def main():
    print(parse_input(sys.stdin.read()))


if __name__ == "__main__":
    main()
