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


RE = re.compile(r"^(?P<min>\d+)-(?P<max>\d+) (?P<letter>[a-z])$")


class Policy(NamedTuple):
    min: int
    max: int
    letter: str

    @classmethod
    def from_string(cls, s):
        parsed = RE.match(s).groupdict()
        return cls(
            min=int(parsed["min"]), max=int(parsed["max"]), letter=parsed["letter"]
        )

    def is_valid(self, password):
        return self.min <= password.count(self.letter) <= self.max


def part1(passwords):
    """
    Count how many passwords are valid according to their policy
    """
    return sum(1 for policy, password in passwords if policy.is_valid(password))


if __name__ == "__main__":
    passwords = load_passwords()
    print(part1(passwords))
