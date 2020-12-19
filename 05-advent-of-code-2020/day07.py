import re
from textwrap import dedent

import pytest


@pytest.fixture
def sample_rules():
    return parse_rules(
        dedent(
            """\
            light red bags contain 1 bright white bag, 2 muted yellow bags.
            dark orange bags contain 3 bright white bags, 4 muted yellow bags.
            bright white bags contain 1 shiny gold bag.
            muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
            shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
            dark olive bags contain 3 faded blue bags, 4 dotted black bags.
            vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
            faded blue bags contain no other bags.
            dotted black bags contain no other bags.
            """
        )
    )


def test_parse_rules(sample_rules):
    assert sample_rules == [
        ("light red", {(1, "bright white"), (2, "muted yellow")}),
        ("dark orange", {(3, "bright white"), (4, "muted yellow")}),
        ("bright white", {(1, "shiny gold")}),
        ("muted yellow", {(2, "shiny gold"), (9, "faded blue")}),
        ("shiny gold", {(1, "dark olive"), (2, "vibrant plum")}),
        ("dark olive", {(3, "faded blue"), (4, "dotted black")}),
        ("vibrant plum", {(5, "faded blue"), (6, "dotted black")}),
        ("faded blue", set()),
        ("dotted black", set()),
    ]


def parse_rules(text):
    return [parse_rule(line.strip()) for line in text.splitlines()]


def parse_rule(line):
    mo = re.match(r"(.+) bags contain (.+)\.$", line)
    return mo.group(1), parse_contents(mo.group(2))


def parse_contents(text):
    if text == "no other bags":
        return set()
    return {parse_part(part) for part in text.split(", ")}


def parse_part(part):
    mo = re.match(r"(\d+) (.+) bags?$", part)
    return int(mo.group(1)), mo.group(2)


def test_possible_containers(sample_rules):
    assert possible_containers(sample_rules, "shiny gold") == {
        "bright white",
        "muted yellow",
        "dark orange",
        "light red",
    }


def possible_containers(rules, target_bag_type):
    result = set()
    for container, contents in rules:
        for number, bag_type in contents:
            if bag_type == target_bag_type and container not in result:
                result.add(container)
                result |= possible_containers(rules, container)
    return result


if __name__ == "__main__":
    with open("day07.txt") as f:
        rules = parse_rules(f.read())
    print("Part 1:", len(possible_containers(rules, "shiny gold")))
