# https://adventofcode.com/2023/day/16
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pytest

from grid import Coords, Grid, Direction


EXAMPLE = """\
.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....
"""


def test_grid():
    grid = Grid.from_string(EXAMPLE)
    assert grid.width == 10
    assert grid.height == 10


@pytest.fixture
def grid():
    return Grid.from_string(EXAMPLE)


class TestMoveBeam:
    def test_move_through_empty_space(self, grid: Grid):
        beam = Beam()

        new_beams = beam.move(grid)

        assert new_beams == {Beam(position=Coords(2, 1), direction=Direction.RIGHT)}

    def test_reflect_in_mirror(self, grid: Grid):
        beam = Beam(position=Coords(6, 1))

        assert beam.position == Coords(6, 1)
        assert beam.direction == Direction.RIGHT
        assert grid.at(6 - 1, 1 - 1) == "\\"

        new_beams = beam.move(grid)

        assert new_beams == {Beam(position=Coords(6, 2), direction=Direction.DOWN)}

    def test_splitter(self, grid: Grid):
        beam = Beam(position=Coords(8, 8))
        assert grid.at(8 - 1, 8 - 1) == "|"
        new_beams = beam.move(grid)
        assert new_beams == {
            Beam(position=Coords(8, 7), direction=Direction.UP),
            Beam(position=Coords(8, 9), direction=Direction.DOWN),
        }

    def test_splitter_on_the_edge(self, grid: Grid):
        beam = Beam(position=Coords(2, 1))
        assert grid.at(2 - 1, 1 - 1) == "|"
        new_beams = beam.move(grid)
        assert new_beams == {Beam(position=Coords(2, 2), direction=Direction.DOWN)}


@dataclass(frozen=True)
class Beam:
    position: Coords = Coords(1, 1)
    direction: Direction = Direction.RIGHT

    def is_in(self, grid: Grid) -> bool:
        return (1 <= self.position.x <= grid.width) and (
            1 <= self.position.y <= grid.height
        )

    def move(self, grid: Grid) -> set[Beam]:
        char = grid.at(self.position.x - 1, self.position.y - 1)
        match char:
            case ".":
                beams = self.move_through()
            case "\\" | "/":
                beams = self.reflect(char)
            case "|":
                match self.direction:
                    case Direction.UP | Direction.DOWN:
                        beams = self.move_through()
                    case _:
                        beams = self.split(char)
            case "-":
                match self.direction:
                    case Direction.LEFT | Direction.RIGHT:
                        beams = self.move_through()
                    case _:
                        beams = self.split(char)
            case _:
                raise NotImplementedError
        return {beam for beam in beams if beam.is_in(grid)}

    def move_through(self) -> set[Beam]:
        return {Beam(position=self.position + self.direction, direction=self.direction)}

    def reflect(self, char: Literal["\\", "/"]) -> set[Beam]:
        match char, self.direction:
            case ("\\", Direction.LEFT) | ("\\", Direction.RIGHT):
                direction = self.rotate_right()
            case ("\\", Direction.UP) | ("\\", Direction.DOWN):
                direction = self.rotate_left()
            case ("/", Direction.UP) | ("/", Direction.DOWN):
                direction = self.rotate_right()
            case ("/", Direction.LEFT) | ("/", Direction.RIGHT):
                direction = self.rotate_left()
            case _:
                raise NotImplementedError
        return {Beam(position=self.position + direction, direction=direction)}

    def split(self, char: Literal["-", "|"]) -> set[Beam]:
        match char:
            case "|":
                directions = (Direction.UP, Direction.DOWN)
            case "-":
                directions = (Direction.LEFT, Direction.RIGHT)
        return {
            Beam(position=self.position + direction, direction=direction)
            for direction in directions
        }

    def rotate_left(self) -> Direction:
        match self.direction:
            case Direction.RIGHT:
                return Direction.UP
            case Direction.DOWN:
                return Direction.RIGHT
            case Direction.LEFT:
                return Direction.DOWN
            case Direction.UP:
                return Direction.LEFT

    def rotate_right(self) -> Direction:
        match self.direction:
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP
            case Direction.UP:
                return Direction.RIGHT


class Cave:
    grid: Grid
    beams: set[Beam]


def test_part1():
    assert part1(EXAMPLE) == 46


def part1(text: str) -> int:
    grid = Grid.from_string(text)
    return number_of_activated_tiles(grid=grid, initial=Beam())


def number_of_activated_tiles(grid: Grid, initial: Beam) -> int:
    beams: set[Beam] = set()
    new_beams = {initial}
    while new_beams:
        input_ = new_beams.pop()
        beams.add(input_)
        for output_ in input_.move(grid):
            if output_ not in beams:
                new_beams.add(output_)
    activated = {beam.position for beam in beams}
    return len(activated)


def test_part2():
    assert part2(EXAMPLE) == 51


def part2(text: str) -> int:
    grid = Grid.from_string(text)
    top_beams = [
        Beam(position=Coords(x, 1), direction=Direction.DOWN)
        for x in range(1, grid.width + 1)
    ]
    bottom_beams = [
        Beam(position=Coords(x, grid.height), direction=Direction.UP)
        for x in range(1, grid.width + 1)
    ]
    left_beams = [
        Beam(position=Coords(1, y), direction=Direction.RIGHT)
        for y in range(1, grid.height + 1)
    ]
    right_beams = [
        Beam(position=Coords(grid.width, y), direction=Direction.LEFT)
        for y in range(1, grid.height + 1)
    ]
    beams = top_beams + bottom_beams + left_beams + right_beams
    return max(number_of_activated_tiles(grid=grid, initial=beam) for beam in beams)


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
    print("Part 2", part2(puzzle_input))
