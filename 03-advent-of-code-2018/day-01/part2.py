#!/usr/bin/env python
import sys
from itertools import cycle


def find_first_repeating_freq(frequency_changes):
    seen = set()
    freq = 0
    for change in cycle(frequency_changes):
        freq += change
        if freq in seen:
            return freq
        seen.add(freq)


def read_input():
    yield from (int(line) for line in sys.stdin)


if __name__ == '__main__':
    frequency_changes = read_input()
    print(find_first_repeating_freq(frequency_changes))
