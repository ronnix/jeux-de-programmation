from textwrap import dedent

from more_itertools import quantify

import pytest


@pytest.fixture
def sample_input():
    return dedent(
        """\
        L.LL.LL.LL
        LLLLLLL.LL
        L.L.L..L..
        LLLL.LL.LL
        L.LL.LL.LL
        L.LLLLL.LL
        ..L.L.....
        LLLLLLLLLL
        L.LLLLLL.L
        L.LLLLL.LL"""
    )


@pytest.fixture
def sample_grid(sample_input):
    return Grid.from_text(sample_input)


def test_grid(sample_grid, sample_input):
    assert sample_grid.to_text() == sample_input


def test_first_step(sample_grid):
    assert sample_grid.next_step().to_text() == dedent(
        """\
        #.##.##.##
        #######.##
        #.#.#..#..
        ####.##.##
        #.##.##.##
        #.#####.##
        ..#.#.....
        ##########
        #.######.#
        #.#####.##"""
    )


def test_second_step(sample_grid):
    assert sample_grid.next_step().next_step().to_text() == dedent(
        """\
        #.LL.L#.##
        #LLLLLL.L#
        L.L.L..L..
        #LLL.LL.L#
        #.LL.LL.LL
        #.LLLL#.##
        ..L.L.....
        #LLLLLLLL#
        #.LLLLLL.L
        #.#LLLL.##"""
    )


def test_fifth_step(sample_grid):
    grid = sample_grid
    for _ in range(5):
        grid = grid.next_step()
    assert grid.to_text() == dedent(
        """\
        #.#L.L#.##
        #LLL#LL.L#
        L.#.L..#..
        #L##.##.L#
        #.#L.LL.LL
        #.#L#L#.##
        ..L.L.....
        #L#L##L#L#
        #.LLLLLL.L
        #.#L#L#.##"""
    )


def test_number_of_stable_occupied_seats(sample_grid):
    assert number_of_stable_occupied_seats(sample_grid) == 37


def number_of_stable_occupied_seats(grid):
    while True:
        next_ = grid.next_step()
        if next_ == grid:
            break
        grid = next_
    return grid.number_of_occupied_seats()


class Grid:
    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        return self.data == other.data

    def at(self, x, y):
        return self.data[y][x]

    def number_of_occupied_seats(self):
        return sum(line.count("#") for line in self.data)

    def adjacent_seats(self, x, y):
        for x_offset in (-1, 0, 1):
            for y_offset in (-1, 0, 1):
                ax = x + x_offset
                ay = y + y_offset
                if (
                    0 <= ax < self.width
                    and 0 <= ay < self.height
                    and (ax, ay) != (x, y)
                ):
                    yield ax, ay

    def number_of_occupied_adjacent_seats(self, x, y):
        return quantify(self.adjacent_seats(x, y), lambda c: self.at(*c) == "#")

    def next_state(self, x, y):
        current = self.at(x, y)
        if current == ".":
            return "."
        nb = self.number_of_occupied_adjacent_seats(x, y)
        if current == "L" and nb == 0:
            return "#"
        elif current == "#" and nb >= 4:
            return "L"
        else:
            return current

    def next_step(self):
        return Grid(
            [
                "".join(self.next_state(x, y) for x in range(self.width))
                for y in range(self.height)
            ]
        )

    @property
    def width(self):
        return len(self.data[0])

    @property
    def height(self):
        return len(self.data)

    @classmethod
    def from_text(cls, text):
        return cls([line.strip() for line in text.splitlines() if line])

    def to_text(self):
        return "\n".join(self.data)


def part1(grid):
    return number_of_stable_occupied_seats(grid)


if __name__ == "__main__":
    with open("day11.txt") as f:
        grid = Grid.from_text(f.read())
    print("Part 1:", part1(grid))
