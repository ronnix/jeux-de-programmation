# https://adventofcode.com/2021/day/10

from dataclasses import dataclass
from typing import List


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


def test_corrupted_lines() -> None:
    parsed_lines = [(line, parse_line(line)) for line in SAMPLE_INPUT.splitlines()]
    corrupted_lines = [line for line, result in parsed_lines if result.corrupted]
    assert corrupted_lines == [
        "{([(<{}[<>[]}>{[]{[(<()>",
        "[[<[([]))<([[{}[[()]]]",
        "[{[{({}]{}}([{[{{{}}([]",
        "[<(<(<(<{}))><([]([]()",
        "<{([([[(<>()){}]>(<<{{",
    ]


def test_part1() -> None:
    syntax_error_score = part1(SAMPLE_INPUT.splitlines())
    assert syntax_error_score == 26397


def part1(lines: List[str]) -> int:
    return syntax_error_score(lines)


def syntax_error_score(lines: List[str]) -> int:
    return sum(parse_line(line).score for line in lines)


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


@dataclass
class ParseResult:
    corrupted: bool
    message: str = ""
    score: int = 0


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
    return ParseResult(corrupted=False)


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    lines = read_input().splitlines()
    print("Part 1:", part1(lines))
