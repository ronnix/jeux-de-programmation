#!/usr/bin/env python
import sys


def test_read_input():
    res = read_input(["183, 157\n", "331, 86\n"])
    assert list(res) == [(183, 157), (331, 86)]


def read_input(stream):
    return (tuple(map(int, line.strip().split(", "))) for line in stream)


def main():
    print(list(read_input(sys.stdin)))


if __name__ == "__main__":
    main()
