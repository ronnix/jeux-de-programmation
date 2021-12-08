# https://adventofcode.com/2021/day/8

from typing import FrozenSet, List, Set, Tuple


SHORT_INPUT = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"

LONGER_INPUT = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

CORRECT_PATTERNS = {
    0: set("abcefg"),   # 6 segments
    1: set("cf"),       # 2 segments
    2: set("acdeg"),    # 5 segments
    3: set("acdfg"),    # 5 segments
    4: set("bcdf"),     # 4 segments
    5: set("abdfg"),    # 5 segments
    6: set("abdefg"),   # 6 segments
    7: set("acf"),      # 3 segments
    8: set("abcdefg"),  # 7 segments
    9: set("abcdfg"),   # 6 segments
}

Entry = Tuple[Set[FrozenSet[str]], List[FrozenSet[str]]]


# === Part 1 ===


def test_parsing() -> None:
    entries = parse(SHORT_INPUT)
    assert isinstance(entries, list)
    assert len(entries) == 1

    entry = entries[0]
    assert isinstance(entry, tuple)
    assert len(entry) == 2

    unique_signal_patterns, output_value = entry
    assert isinstance(unique_signal_patterns, set)
    assert len(unique_signal_patterns) == 10
    assert unique_signal_patterns == {
        frozenset("acedgfb"),
        frozenset("cdfbe"),
        frozenset("gcdfa"),
        frozenset("fbcad"),
        frozenset("dab"),
        frozenset("cefabd"),
        frozenset("cdfgeb"),
        frozenset("eafb"),
        frozenset("cagedb"),
        frozenset("ab"),
    }

    assert output_value == [
            frozenset("cdfeb"),
            frozenset("fcadb"),
            frozenset("cdfeb"),
            frozenset("cdbaf"),
        ]


def test_part1() -> None:
    assert part1(parse(LONGER_INPUT)) == 26


def part1(entries: List[Entry]) -> int:
    return count_digits(entries, {1, 4, 7, 8})


def count_digits(entries: List[Entry], digits: Set[int]) -> int:
    return sum(count_digit(entries, digit) for digit in digits)


def count_digit(entries: List[Entry], digit: int) -> int:
    count = 0
    for signal_patterns, output_value in entries:
        segments = find_matching_segments_for(signal_patterns, digit)
        count += sum(1 for v in output_value if v == segments)
    return count


def find_matching_segments_for(signal_patterns: Set[FrozenSet[str]], digit: int) -> FrozenSet[str]:
    for pattern in signal_patterns:
        if len(pattern) == len(CORRECT_PATTERNS[digit]):
            return pattern
    raise ValueError


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> List[Entry]:
    return [parse_entry(line) for line in text.splitlines()]


def parse_entry(line: str) -> Entry:
    left, right = line.split(" | ")
    unique_signal_patterns = parse_unique_signal_patterns(left)
    output_value = parse_output_value(right)
    return (unique_signal_patterns, output_value)


def parse_unique_signal_patterns(text: str) -> Set[FrozenSet[str]]:
    return {frozenset(letters) for letters in text.split(" ")}


def parse_output_value(text: str) -> List[FrozenSet[str]]:
    return [frozenset(letters) for letters in text.split(" ")]


if __name__ == "__main__":
    entries = parse(read_input())
    print("Part 1:", part1(entries))
