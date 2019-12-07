import re

import pytest


@pytest.mark.parametrize("password", ["1111111",])
def test_matches(password):
    assert matches(password)


@pytest.mark.parametrize("password", ["223450", "123789",])
def test_not_matches(password):
    assert not matches(password)


def matches(password):
    if not re.search(r"(?P<digit>[0-9])(?P=digit)", password):  # 2 identical digits
        return False
    digits = (int(char) for char in password)
    previous = 0
    for digit in digits:
        if digit < previous:
            return False
        previous = digit
    return True


def part1(lower, upper):
    return sum(1 for n in range(lower, upper + 1) if matches(str(n)))


if __name__ == "__main__":
    print("Part 1:", part1(152085, 670283))
