# https://adventofcode.com/2021/day/8

from typing import Dict, FrozenSet, List, Set, Tuple

from constraint import AllDifferentConstraint, InSetConstraint, Problem

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

DIGIT_TO_SEGMENTS = {
    0: frozenset("abcefg"),
    1: frozenset("cf"),
    2: frozenset("acdeg"),
    3: frozenset("acdfg"),
    4: frozenset("bcdf"),
    5: frozenset("abdfg"),
    6: frozenset("abdefg"),
    7: frozenset("acf"),
    8: frozenset("abcdefg"),
    9: frozenset("abcdfg"),
}

SEGMENTS_TO_DIGIT = {v: k for k, v in DIGIT_TO_SEGMENTS.items()}

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
        segments = find_possible_signals_for(signal_patterns, digit)
        count += sum(1 for v in output_value if v == segments)
    return count


def find_possible_signals_for(
    signal_patterns: Set[FrozenSet[str]], digit: int
) -> FrozenSet[str]:
    for pattern in signal_patterns:
        if len(pattern) == len(DIGIT_TO_SEGMENTS[digit]):
            return pattern
    raise ValueError


# === Part 2 ===


def test_part2_short() -> None:
    entry = parse_entry(SHORT_INPUT)
    assert part2([entry]) == 5353


def test_part2_longer() -> None:
    entries = parse(LONGER_INPUT)
    assert part2(entries) == 61229


def part2(entries: List[Entry]) -> int:
    return sum(solve_entry(entry) for entry in entries)


def solve_entry(entry: Entry) -> int:
    signal_patterns, output_value = entry
    mapping = find_mapping(signal_patterns)
    return int("".join(translate_signal(signal, mapping) for signal in output_value))


def translate_signal(value: FrozenSet[str], mapping: Dict[str, str]) -> str:
    segments = frozenset(mapping[signal] for signal in value)
    return str(SEGMENTS_TO_DIGIT[segments])


def test_find_mapping() -> None:
    signal_patterns, _ = parse_entry(SHORT_INPUT)
    mapping = find_mapping(signal_patterns)
    assert mapping == {
        "a": "c",
        "b": "f",
        "c": "g",
        "d": "a",
        "e": "b",
        "f": "d",
        "g": "e",
    }


def find_mapping(signal_patterns: Set[FrozenSet[str]]) -> Dict[str, str]:

    # Let’s express this as a constraint satisfaction problem
    problem = Problem()
    for signal in "abcdefg":
        problem.addVariable(signal, "abcdefg")

    # Each signal wire goes to a different segment
    problem.addConstraint(AllDifferentConstraint())

    # Unambiguous digits based on count of lit segments
    for digit in {1, 4, 7, 8}:
        for wire in find_possible_signals_for(signal_patterns, digit):
            segments = DIGIT_TO_SEGMENTS[digit]
            problem.addConstraint(InSetConstraint(segments), wire)

    # Unambiguous segments based on how many times they appear in patterns
    for signal_wire in {"a", "b", "c", "d", "e", "f", "g"}:
        count = sum(1 for pattern in signal_patterns if signal_wire in pattern)
        if count == 4:
            problem.addConstraint(InSetConstraint(["e"]), signal_wire)
        elif count == 6:
            problem.addConstraint(InSetConstraint(["b"]), signal_wire)
        elif count == 7:
            problem.addConstraint(InSetConstraint(["d", "g"]), signal_wire)
        elif count == 8:
            problem.addConstraint(InSetConstraint(["a", "c"]), signal_wire)
        elif count == 9:
            problem.addConstraint(InSetConstraint(["f"]), signal_wire)
        else:
            raise ValueError

    return problem.getSolution()


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
    print("Part 2:", part2(entries))
