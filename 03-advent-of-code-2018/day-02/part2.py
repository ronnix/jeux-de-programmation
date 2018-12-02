#!/usr/bin/env python
import sys
from itertools import combinations


def read_input():
    return sys.stdin.read().splitlines()


def common_letters(word1, word2):
    return [l1 for l1, l2 in zip(word1, word2) if l1 == l2]


if __name__ == "__main__":
    box_ids = read_input()
    for box_id1, box_id2 in combinations(box_ids, 2):
        common = common_letters(box_id1, box_id2)
        nb_diff = len(box_id1) - len(common)
        if nb_diff == 1:
            print("".join(common))
