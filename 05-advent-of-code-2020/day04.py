from textwrap import dedent

from more_itertools import split_at

import pytest


@pytest.fixture
def sample_batch():
    return read_batch(
        dedent(
            """\
            ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
            byr:1937 iyr:2017 cid:147 hgt:183cm

            iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
            hcl:#cfa07d byr:1929

            hcl:#ae17e1 iyr:2013
            eyr:2024
            ecl:brn pid:760753108 byr:1931
            hgt:179cm

            hcl:#cfa07d eyr:2025 pid:166559648
            iyr:2011 ecl:brn hgt:59in
            """
        )
    )


def read_batch(text):
    return [
        Passport(" ".join(lines))
        for lines in split_at(text.splitlines(), lambda line: line == "")
    ]


class Passport:
    REQUIRED_FIELDS = {
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
    }

    def __init__(self, text):
        self.fields = dict(field.split(":") for field in text.split(" "))

    def is_valid(self):
        return Passport.REQUIRED_FIELDS.issubset(self.fields.keys())


def test_valid_passports(sample_batch):
    assert len([passport for passport in sample_batch if passport.is_valid()]) == 2


if __name__ == "__main__":
    with open("day04.txt") as f:
        batch = read_batch(f.read())
    print("Part 1:", len([passport for passport in batch if passport.is_valid()]))
