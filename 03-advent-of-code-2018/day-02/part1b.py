#!/usr/bin/env python
import sys
from collections import Counter


def read_input():
    return sys.stdin.read().splitlines()


def has_a_letter_repeating_n_times(n, counter):
    return any((count == n) for count in counter.values())


if __name__ == "__main__":
    counters = [Counter(s) for s in read_input()]
    twos = (
        counter
        for counter in counters
        if has_a_letter_repeating_n_times(2, counter)
    )
    threes = (
        counter
        for counter in counters
        if has_a_letter_repeating_n_times(3, counter)
    )
    print(len(list(twos)) * len(list(threes)))
