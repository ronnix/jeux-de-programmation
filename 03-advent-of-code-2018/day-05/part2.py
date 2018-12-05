#!/usr/bin/env python
import sys

from part1 import reduce_polymer


def test_gen_modified_polymers():
    assert set(gen_modified_polymers("dabAcCaCBAcCcaDA")) == {
        "dbcCCBcCcD",
        "daAcCaCAcCcaDA",
        "dabAaBAaDA",
        "abAcCaCBAcCcaA",
    }


def gen_modified_polymers(polymer):
    for unit_to_remove in set(polymer.lower()):
        yield "".join(unit for unit in polymer if unit.lower() != unit_to_remove)


def main():
    print(
        min(
            len(reduce_polymer(modified_polymer))
            for modified_polymer in gen_modified_polymers(sys.stdin.read())
        )
    )


if __name__ == "__main__":
    main()
