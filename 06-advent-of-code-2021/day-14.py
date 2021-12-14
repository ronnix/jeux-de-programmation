# https://adventofcode.com/2021/day/14

from collections import Counter
from functools import partial
from typing import Dict, Iterator, Sequence, Tuple

from more_itertools import windowed


SAMPLE_INPUT = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


# === Part 1 ===

Rule = Tuple[Tuple[str, str], str]
Rules = Dict[Tuple[str, str], str]


def test_parsing() -> None:
    template, rules = parse(SAMPLE_INPUT)
    assert template == "NNCB"
    assert rules[("C", "H")] == "B"


def test_apply() -> None:
    template, rules = parse(SAMPLE_INPUT)
    assert apply(rules, template) == "NCNBCHB"


def apply(rules: Rules, polymer: str) -> str:
    return "".join(_apply(rules, polymer))


def _apply(rules: Rules, polymer: str) -> Iterator[str]:
    for pair in windowed(polymer, 2):
        yield pair[0]
        if pair in rules:
            yield rules[pair]
    yield polymer[-1]


def test_repeat_apply() -> None:
    template, rules = parse(SAMPLE_INPUT)
    assert (
        repeat(partial(apply, rules), 4, template)
        == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
    )


def repeat(func, n, arg):
    for _ in range(n):
        arg = func(arg)
    return arg


def test_part1() -> None:
    template, rules = parse(SAMPLE_INPUT)
    assert part1(template, rules) == 1588


def part1(template: str, rules: Rules) -> int:
    polymer = repeat(partial(apply, rules), 10, template)
    counts: Sequence[Tuple[str, int]] = Counter(polymer).most_common(None)
    most_common = counts[0][1]
    least_common = counts[-1][1]
    return most_common - least_common


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> Tuple[str, Rules]:
    polymer_template, rules = text.split("\n\n", 1)
    return polymer_template, dict(parse_rule(line) for line in rules.splitlines())


def parse_rule(line: str) -> Rule:
    left, right = line.split(" -> ")
    return ((left[0], left[1]), right)


if __name__ == "__main__":
    print("Part 1:", part1(*parse(read_input())))
