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
    claims = list(read_input())

    # Build the fabric overlap map
    for claim in claims:
        for x, y in claim.covered_squares():
            fabric[(x, y)] += 1

    # Find the first claim with no overlap
    for claim in claims:
        if all(
            fabric[(x, y)] == 1
            for x, y in claim.covered_squares()
        ):
            print(claim.id)
            break
    else:
        print("Not found")
