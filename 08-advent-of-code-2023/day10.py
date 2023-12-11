# https://adventofcode.com/2023/day/10
from __future__ import annotations
from ast import Name

from dataclasses import dataclass
from enum import Enum
from tkinter import HORIZONTAL
from typing import Iterator, List, NamedTuple

import networkx as nx

import pytest


EXAMPLE_TILES = """\
.....
.S-7.
.|.|.
.L-J.
.....
"""


def test_parse_tiles():
    t = Tiles.from_string(EXAMPLE_TILES)
    assert t.width == 5
    assert t.height == 5


def test_find_start():
    t = Tiles.from_string(EXAMPLE_TILES)
    assert t.start() == Coords(1, 1)


def test_neighbors():
    t = Tiles.from_string(EXAMPLE_TILES)
    assert list(t.neighbors(Coords(1, 1))) == [
        Coords(x=0, y=1),
        Coords(x=2, y=1),
        Coords(x=1, y=0),
        Coords(x=1, y=2),
    ]


def test_connects_to():
    t = Tiles.from_string(EXAMPLE_TILES)
    assert set(t.connects_to(Coords(1, 2))) == {Coords(x=1, y=1), Coords(x=1, y=3)}
    assert set(t.connects_to(Coords(2, 1))) == {Coords(x=1, y=1), Coords(x=3, y=1)}


def test_find_graph():
    t = Tiles.from_string(EXAMPLE_TILES)
    g = t.graph()
    assert set(g.nodes) == {
        Coords(x=1, y=1),
        Coords(x=1, y=2),
        Coords(x=1, y=3),
        Coords(x=2, y=1),
        Coords(x=2, y=3),
        Coords(x=3, y=1),
        Coords(x=3, y=2),
        Coords(x=3, y=3),
    }
    assert set(g.edges) == {
        (Coords(x=1, y=1), Coords(x=1, y=2)),
        (Coords(x=1, y=1), Coords(x=2, y=1)),
        (Coords(x=1, y=3), Coords(x=1, y=2)),
        (Coords(x=2, y=1), Coords(x=3, y=1)),
        (Coords(x=2, y=3), Coords(x=1, y=3)),
        (Coords(x=3, y=1), Coords(x=3, y=2)),
        (Coords(x=3, y=2), Coords(x=3, y=3)),
        (Coords(x=3, y=3), Coords(x=2, y=3)),
    }


def test_diameter():
    t = Tiles.from_string(EXAMPLE_TILES)
    g = t.graph()
    assert nx.diameter(g) == 4


class Coords(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    N = (0, -1)
    S = (0, +1)
    W = (-1, 0)
    E = (+1, 0)


TILES = {
    "|": (Direction.N, Direction.S),
    "-": (Direction.W, Direction.E),
    "L": (Direction.N, Direction.E),
    "J": (Direction.N, Direction.W),
    "7": (Direction.S, Direction.W),
    "F": (Direction.S, Direction.E),
}


@dataclass(frozen=True)
class Tiles:
    grid: List[str]

    @property
    def width(self) -> int:
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)

    def start(self) -> Coords:
        for y, line in enumerate(self.grid):
            for x, char in enumerate(line):
                if char == "S":
                    return Coords(x, y)
        raise ValueError

    def neighbors(self, c: Coords) -> Iterator[Coords]:
        for dx in [-1, +1]:
            if 0 <= c.x + dx < self.width:
                yield Coords(c.x + dx, c.y)
        for dy in [-1, +1]:
            if 0 <= c.y + dy < self.height:
                yield Coords(c.x, c.y + dy)

    def connects_to(self, c: Coords) -> Iterator[Coords]:
        tile = self.grid[c.y][c.x]
        for direction in TILES.get(tile, []):
            dx, dy = direction.value
            yield Coords(c.x + dx, c.y + dy)

    def graph(self) -> nx.Graph:
        start: Coords = self.start()
        graph = nx.Graph()
        graph.add_node(start)
        for neighbor in self.neighbors(start):
            if start in set(self.connects_to(neighbor)):
                graph.add_node(neighbor)
                graph.add_edge(start, neighbor)
                node = neighbor
                while True:
                    try:
                        succ = next(
                            node
                            for node in self.connects_to(node)
                            if node not in graph.nodes
                        )
                    except StopIteration:
                        break
                    graph.add_node(succ)
                    graph.add_edge(node, succ)
                    node = succ
        return graph

    @classmethod
    def from_string(cls, text: str) -> Tiles:
        return cls(grid=text.strip().splitlines())


def test_part1():
    assert part1(EXAMPLE_TILES) == 4


def part1(text: str) -> int:
    t = Tiles.from_string(text)
    return nx.diameter(t.graph())


def read_puzzle_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
