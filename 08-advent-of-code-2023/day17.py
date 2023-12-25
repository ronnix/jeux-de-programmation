# https://adventofcode.com/2023/day/17
from __future__ import annotations

from typing import NamedTuple, Self

import networkx as nx

from grid import Coords, Grid, Direction, Orientation

import pytest

EXAMPLE = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""


@pytest.fixture
def grid():
    return Grid.from_string(EXAMPLE)


def test_graph():
    graph = Graph.from_string(EXAMPLE)
    assert graph.width == 13
    assert graph.height == 13
    assert len(graph.nodes) == 13 * 13 * 2


class Node(NamedTuple):
    position: Coords
    orientation: Orientation


class Graph(nx.DiGraph):
    def __init__(self, grid: Grid) -> None:
        super().__init__()
        self._grid = grid

    @property
    def width(self):
        return self._grid.width

    @property
    def height(self):
        return self._grid.height

    @classmethod
    def from_string(cls, text: str, min_dist: int = 1, max_dist: int = 3) -> Self:
        graph = cls(grid=Grid.from_string(text))
        for y in range(graph._grid.height):
            for x in range(graph._grid.width):
                for orientation in (Orientation.HORIZONTAL, Orientation.VERTICAL):
                    node = Node(position=Coords(x, y), orientation=orientation)
                    match orientation:
                        case Orientation.HORIZONTAL:
                            directions = [Direction.LEFT, Direction.RIGHT]
                            next_orientation = Orientation.VERTICAL
                        case Orientation.VERTICAL:
                            directions = [Direction.UP, Direction.DOWN]
                            next_orientation = Orientation.HORIZONTAL
                    for direction in directions:
                        for length in range(min_dist, max_dist + 1):
                            next_node = Node(
                                position=node.position + direction.value * length,
                                orientation=next_orientation,
                            )
                            if (
                                0 <= next_node.position.x < graph._grid.width
                                and 0 <= next_node.position.y < graph._grid.height
                            ):
                                heat_loss = sum(
                                    int(
                                        graph._grid.at(
                                            *(node.position + direction.value * i)
                                        )
                                    )
                                    for i in range(1, length + 1)
                                )
                                graph.add_edge(node, next_node, heat_loss=heat_loss)
        return graph

    def minimum_heat_loss(self) -> int:
        return min(
            self._minimum_heat_loss(source_orientation, dest_orientation)
            for source_orientation in [Orientation.HORIZONTAL, Orientation.VERTICAL]
            for dest_orientation in [Orientation.HORIZONTAL, Orientation.VERTICAL]
        )

    def _minimum_heat_loss(
        self, source_orientation: Orientation, dest_orientation: Orientation
    ) -> int:
        return nx.shortest_path_length(
            self,
            source=Node(position=Coords(0, 0), orientation=source_orientation),
            target=Node(
                position=Coords(self.width - 1, self.height - 1),
                orientation=dest_orientation,
            ),
            weight="heat_loss",
        )


def test_part1():
    assert part1(EXAMPLE) == 102


def part1(text: str) -> int:
    graph = Graph.from_string(text)
    return graph.minimum_heat_loss()


def test_part2():
    assert part2(EXAMPLE) == 94


OTHER_EXAMPLE = """\
111111111111
999999999991
999999999991
999999999991
999999999991
"""


def test_part2_other_example():
    assert part2(OTHER_EXAMPLE) == 71


def part2(text: str) -> int:
    graph = Graph.from_string(text, min_dist=4, max_dist=10)
    return graph.minimum_heat_loss()


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    puzzle_input = read_puzzle_input()
    print("Part 1", part1(puzzle_input))
    print("Part 2", part2(puzzle_input))
