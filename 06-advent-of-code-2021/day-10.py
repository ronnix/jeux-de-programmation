# https://adventofcode.com/2021/day/10

from dataclasses import dataclass
from functools import reduce
from typing import List

import pytest

SAMPLE_INPUT = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


# === Part 1 ===


@pytest.fixture
def lines() -> List[str]:
    return SAMPLE_INPUT.splitlines()


def test_corrupted_lines(lines: List[str]) -> None:
    corrupted_lines = [
        line for line, result in zip(lines, parse_lines(lines)) if result.corrupted
    ]
    assert corrupted_lines == [
        "{([(<{}[<>[]}>{[]{[(<()>",
        "[[<[([]))<([[{}[[()]]]",
        "[{[{({}]{}}([{[{{{}}([]",
        "[<(<(<(<{}))><([]([]()",
        "<{([([[(<>()){}]>(<<{{",
    ]


@dataclass
class ParseResult:
    corrupted: bool
    message: str = ""
    missing: str = ""
    score: int = 0


def parse_lines(lines: List[str]) -> List[ParseResult]:
    return [parse_line(line) for line in lines]


def test_syntax_error_score(lines: List[str]) -> None:
    assert syntax_error_score(lines) == 26397


def syntax_error_score(lines: List[str]) -> int:
    results = parse_lines(lines)
    return sum(result.score for result in results if result.corrupted)


def part1(lines: List[str]) -> int:
    return syntax_error_score(lines)


CLOSING = {
    "(": ")",
    "<": ">",
    "[": "]",
    "{": "}",
}


ERROR_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


COMPLETION_SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def parse_line(line: str) -> ParseResult:
    stack = []
    for char in line:
        if char in "(<[{":
            stack.append(char)
        elif char in ")>]}":
            expected = CLOSING[stack.pop()]
            if char != expected:
                return ParseResult(
                    corrupted=True,
                    message=f"Expected {expected}, but found {char} instead.",
                    score=ERROR_SCORE[char],
                )
    missing = "".join(CLOSING[char] for char in reversed(stack))
    score = reduce(lambda acc, c: acc * 5 + COMPLETION_SCORE[c], missing, 0)
    return ParseResult(corrupted=False, missing=missing, score=score)


# === Part 2 ===


def test_missing_closing_chars(lines: List[str]) -> None:
    results = (parse_line(line) for line in lines)
    missing = [result.missing for result in results if not result.corrupted]
    assert missing == [r"}}]])})]", r")}>]})", r"}}>}>))))", r"]]}}]}]}>", r"])}>"]


def test_completion_scores(lines: List[str]) -> None:
    assert middle(completion_scores(lines)) == 288957


def middle(scores: List[int]) -> int:
    return sorted(scores)[len(scores) // 2]


def completion_scores(lines: List[str]) -> List[int]:
    return [result.score for result in parse_lines(lines) if not result.corrupted]


def part2(lines: List[str]) -> int:
    return middle(completion_scores(lines))


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    lines_ = read_input().splitlines()
    print("Part 1:", part1(lines_))
    print("Part 2:", part2(lines_))
