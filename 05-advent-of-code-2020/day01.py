from itertools import combinations


def load_expenses():
    """
    Read expense report entries from file
    """
    with open("day01.txt") as f:
        return [int(line) for line in f]


def part1(expenses):
    """
    Find expense report entries whose sum is 2020,
    and return their product.
    """
    for e1, e2 in combinations(expenses, 2):
        if e1 + e2 == 2020:
            return e1 * e2


if __name__ == "__main__":
    print(part1(load_expenses()))
