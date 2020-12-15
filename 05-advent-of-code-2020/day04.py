import re
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

    @classmethod
    def validate_byr(cls, value):
        if not re.match(r"\d{4}$", value):
            return False
        return 1920 <= int(value) <= 2002

    @classmethod
    def validate_iyr(cls, value):
        if not re.match(r"\d{4}$", value):
            return False
        return 2010 <= int(value) <= 2020

    @classmethod
    def validate_eyr(cls, value):
        if not re.match(r"\d{4}$", value):
            return False
        return 2020 <= int(value) <= 2030

    @classmethod
    def validate_hgt(cls, value):
        mo = re.match(r"(\d+)(cm|in)$", value)
        if mo is None:
            return False
        number, unit = mo.groups()
        if unit == "cm":
            return 150 <= int(number) <= 193
        else:
            return 59 <= int(number) <= 76

    @classmethod
    def validate_hcl(cls, value):
        return bool(re.match(r"#[0-9a-f]{6}$", value))

    @classmethod
    def validate_ecl(cls, value):
        return bool(re.match(r"(amb|blu|brn|gry|grn|hzl|oth)$", value))

    @classmethod
    def validate_pid(cls, value):
        return bool(re.match(r"\d{9}$", value))

    @classmethod
    def is_valid_for_field(self, key, value):
        return getattr(self, f"validate_{key}")(value)

    def __init__(self, text):
        self.fields = dict(field.split(":") for field in text.split(" "))

    def has_required_fields(self):
        return all(key in self.fields for key in self.REQUIRED_FIELDS)

    def is_valid(self):
        return all(
            key in self.fields and self.is_valid_for_field(key, self.fields[key])
            for key in self.REQUIRED_FIELDS
        )


def test_passwords_with_required_fields(sample_batch):
    assert (
        len([passport for passport in sample_batch if passport.has_required_fields()])
        == 2
    )


@pytest.mark.parametrize(
    "field, is_valid, value",
    [
        ("byr", True, "2002"),
        ("byr", False, "2003"),
        ("hgt", True, "60in"),
        ("hgt", True, "190cm"),
        ("hgt", False, "190in"),
        ("hgt", False, "190"),
        ("hcl", True, "#123abc"),
        ("hcl", False, "#123abz"),
        ("hcl", False, "123abc"),
        ("ecl", True, "brn"),
        ("ecl", False, "wat"),
        ("pid", True, "000000001"),
        ("pid", False, "0123456789"),
    ],
)
def test_field_valid(field, is_valid, value):
    assert Passport.is_valid_for_field(field, value) == is_valid


@pytest.mark.parametrize(
    "text",
    [
        "eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926",
        "iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946",
        "hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277",
        "hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007",
    ],
)
def test_invalid_passports(text):
    assert not Passport(text).is_valid()


@pytest.mark.parametrize(
    "text",
    [
        "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f",
        "eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm",
        "hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022",
        "iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719",
    ],
)
def test_valid_passports(text):
    assert Passport(text).is_valid()


if __name__ == "__main__":
    with open("day04.txt") as f:
        batch = read_batch(f.read())
    print(
        "Part 1:",
        len([passport for passport in batch if passport.has_required_fields()]),
    )
    print(
        "Part 2:",
        len([passport for passport in batch if passport.is_valid()]),
    )
