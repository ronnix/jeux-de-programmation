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

    def is_valid_sled_rental(self, password):
        return self.n1 <= password.count(self.letter) <= self.n2

    def is_valid_toboggan(self, password):
        return (password[self.n1 - 1] == self.letter) ^ (
            password[self.n2 - 1] == self.letter
        )


def part1(passwords):
    """
    Count how many passwords are valid according to the sled rental policy
    """
    return sum(
        1 for policy, password in passwords if policy.is_valid_sled_rental(password)
    )


def part2(passwords):
    """
    Count how many passwords are valid according to the toboggan policy
    """
    return sum(
        1 for policy, password in passwords if policy.is_valid_toboggan(password)
    )


if __name__ == "__main__":
    passwords = load_passwords()
    print("Part 1:", part1(passwords))
    print("Part 2:", part2(passwords))
