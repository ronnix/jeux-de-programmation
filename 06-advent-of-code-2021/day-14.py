# https://adventofcode.com/2021/day/14

from collections import Counter

from typing import Dict, Sequence, Tuple

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

Pair = str
Polymer = Dict[Pair, int]
Rule = Tuple[Pair, Tuple[Pair, Pair]]
Rules = Dict[Pair, Tuple[Pair, Pair]]


def test_parsing() -> None:
    template, rules = parse(SAMPLE_INPUT)
    assert template == {"NN": 1, "NC": 1, "CB": 1, "B.": 1}
    assert rules["CH"] == ("CB", "BH")


def test_apply() -> None:
    template, rules = parse(SAMPLE_INPUT)
    assert apply(rules, template, 1) == parse_polymer("NCNBCHB")
    assert apply(rules, template, 2) == parse_polymer("NBCCNBBBCBHCB")
    assert apply(rules, template, 3) == parse_polymer("NBBBCNCCNBBNBNBBCHBHHBCHB")
    assert apply(rules, template, 4) == parse_polymer(
        "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
    )


def apply(rules: Rules, polymer: Polymer, n: int = 1) -> Polymer:
    for _ in range(n):
        polymer = sum(
            (
                Counter(dict((p, count) for p in rules.get(pair, [pair])))
                for pair, count in polymer.items()
            ),
            Counter(),
        )
    return polymer


def test_part1() -> None:
    template, rules = parse(SAMPLE_INPUT)
    assert part1(template, rules) == 1588


def part1(template: Polymer, rules: Rules) -> int:
    polymer = apply(rules, template, 10)
    return count_most_common_minus_least_common(polymer)


def count_most_common_minus_least_common(polymer: Polymer) -> int:
    letters: Counter = sum(
        (Counter({pair[0]: count}) for pair, count in polymer.items()), Counter()
    )
    counts: Sequence[Tuple[str, int]] = letters.most_common(None)
    most_common = counts[0][1]
    least_common = counts[-1][1]
    return most_common - least_common


# === Part 2 ===


def test_part2() -> None:
    template, rules = parse(SAMPLE_INPUT)
    assert part2(template, rules) == 2188189693529


def part2(template: Polymer, rules: Rules) -> int:
    polymer = apply(rules, template, 40)
    return count_most_common_minus_least_common(polymer)


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> Tuple[Polymer, Rules]:
    template, rules = text.split("\n\n", 1)
    return parse_polymer(template), dict(
        parse_rule(line) for line in rules.splitlines()
    )


def parse_polymer(line: str) -> Polymer:
    return Counter("".join(chars) for chars in windowed(line + ".", 2))


def parse_rule(line: str) -> Rule:
    left, right = line.split(" -> ")
    return (left, (left[0] + right, right + left[1]))


if __name__ == "__main__":
    polymer, rules = parse(read_input())
    print("Part 1:", part1(polymer, rules))
    print("Part 2:", part2(polymer, rules))
