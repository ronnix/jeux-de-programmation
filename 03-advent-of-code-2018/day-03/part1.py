#!/usr/bin/env python
from collections import defaultdict
from typing import NamedTuple
import re
import sys


CLAIM_RE = re.compile(r"#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)")


class Claim(NamedTuple):
    id: int
    x: int
    y: int
    w: int
    h: int

    @classmethod
    def from_string(cls, s):
        values = {
            key: int(value)
            for key, value in CLAIM_RE.match(s).groupdict().items()
        }
        return cls(**values)

    def covered_squares(self):
        return (
            (x, y)
            for x in range(self.x, self.x + self.w)
            for y in range(self.y, self.y + self.h)
        )


def read_input():
    return (
        Claim.from_string(line)
        for line in sys.stdin.read().splitlines()
    )


if __name__ == "__main__":
    fabric = defaultdict(int)
    for claim in read_input():
        for x, y in claim.covered_squares():
            fabric[(x, y)] += 1
    print(len(list(count for count in fabric.values() if count >= 2)))
