# https://adventofcode.com/2023/day/2
from __future__ import annotations

from pathlib import Path
from textwrap import dedent
from typing import Any, NamedTuple, Set
import re

import pytest


EXAMPLE_GAMES = dedent(
    """
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    """
)


def test_part1():
    assert part1(EXAMPLE_GAMES) == 8


class CubeSet(NamedTuple):
    red: int
    green: int
    blue: int

    @classmethod
    def from_string(cls, text: str) -> CubeSet:
        colors = (cubes.split(" ") for cubes in text.split(", "))
        cubes = {color: int(count) for count, color in colors}
        return CubeSet(
            red=cubes.get("red", 0),
            green=cubes.get("green", 0),
            blue=cubes.get("blue", 0),
        )

    def __le__(self, other: Any) -> bool:
        if isinstance(other, CubeSet):
            return (
                self.red <= other.red
                and self.green <= other.green
                and self.blue <= other.blue
            )
        return NotImplemented

    def power(self) -> int:
        return self.red * self.green * self.blue


def test_parse_cubeset():
    r = CubeSet.from_string("3 green, 4 blue, 1 red")
    assert r.red == 1
    assert r.green == 3
    assert r.blue == 4


def test_parse_game():
    g = Game.from_string("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    assert g.id == 1
    assert g.reveals == {
        CubeSet(red=4, green=0, blue=3),
        CubeSet(red=1, green=2, blue=6),
        CubeSet(red=0, green=2, blue=0),
    }


class Game(NamedTuple):
    id: int
    reveals: Set[CubeSet]

    @classmethod
    def from_string(cls, text: str) -> Game:
        game, reveals = text.split(": ")
        mo = re.match(r"Game (\d+)", game)
        assert mo is not None
        return Game(
            id=int(mo.group(1)),
            reveals={CubeSet.from_string(s) for s in reveals.split("; ")},
        )

    def __le__(self, other: Any) -> bool:
        if isinstance(other, CubeSet):
            return all(reveal <= other for reveal in self.reveals)
        return NotImplemented

    def minimum(self) -> CubeSet:
        return CubeSet(
            red=max(cube.red for cube in self.reveals),
            green=max(cube.green for cube in self.reveals),
            blue=max(cube.blue for cube in self.reveals),
        )


def part1(text: str) -> int:
    games = [Game.from_string(line) for line in text.splitlines() if line]
    return sum(game.id for game in games if game <= CubeSet(red=12, green=13, blue=14))


def test_part2():
    assert part2(EXAMPLE_GAMES) == 2286


def part2(text: str) -> int:
    games = [Game.from_string(line) for line in text.splitlines() if line]
    return sum(game.minimum().power() for game in games)


if __name__ == "__main__":
    puzzle_input = Path("day02.txt").read_text()
    print("Part 1", part1(puzzle_input))
    print("Part 2", part2(puzzle_input))
