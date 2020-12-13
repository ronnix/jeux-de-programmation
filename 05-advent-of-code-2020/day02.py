import re
from typing import NamedTuple


def load_passwords():
    """
    Read passwords from file
    """
    with open("day02.txt") as f:
        return [parse_line(line.strip()) for line in f]


def parse_line(line):
    policy_string, password = line.split(": ")
    return Policy.from_string(policy_string), password


RE = re.compile(r"^(?P<n1>\d+)-(?P<n2>\d+) (?P<letter>[a-z])$")


class Policy(NamedTuple):
    n1: int
    n2: int
    letter: str

    @classmethod
    def from_string(cls, s):
        parsed = RE.match(s).groupdict()
        return cls(n1=int(parsed["n1"]), n2=int(parsed["n2"]), letter=parsed["letter"])


def count_valid_passwords(passwords, is_valid):
    """
    Count how many passwords are valid according to a given policy
    """
    return sum(1 for policy, password in passwords if is_valid(policy, password))


def is_valid_sled_rental(policy, password):
    return policy.n1 <= password.count(policy.letter) <= policy.n2


def is_valid_toboggan(policy, password):
    def position_matches(position):
        return password[position - 1] == policy.letter

    return position_matches(policy.n1) ^ position_matches(policy.n2)


def part1(passwords):
    return count_valid_passwords(passwords, is_valid_sled_rental)


def part2(passwords):
    return count_valid_passwords(passwords, is_valid_toboggan)


if __name__ == "__main__":
    passwords = load_passwords()
    print("Part 1:", part1(passwords))
    print("Part 2:", part2(passwords))
