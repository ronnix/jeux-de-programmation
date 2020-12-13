from itertools import combinations
from math import prod


def load_expenses():
    """
    Read expense report entries from file
    """
    with open("day01.txt") as f:
        return [int(line) for line in f]


def find_entries_matching_sum(expenses, nb):
    """
    Find expense report entries whose sum is 2020,
    and return their product.
    """
    for entries in combinations(expenses, nb):
        if sum(entries) == 2020:
            return prod(entries)


def part1(expenses):
    return find_entries_matching_sum(expenses, 2)


def part2(expenses):
    return find_entries_matching_sum(expenses, 3)


if __name__ == "__main__":
    expenses = load_expenses()
    print(part1(expenses))
    print(part2(expenses))
