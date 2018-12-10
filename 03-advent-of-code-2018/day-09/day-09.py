#!/usr/bin/env python
import sys


def test_parse():
    assert parse("426 players; last marble is worth 72058 points") == (426, 72058)


def parse(text):
    words = text.split()
    return int(words[0]), int(words[6])


def main():
    players, points = parse(sys.stdin.read())
    print(players, points)


if __name__ == '__main__':
    main()
