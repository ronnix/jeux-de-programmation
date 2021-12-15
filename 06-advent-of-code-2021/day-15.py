# https://adventofcode.com/2021/day/15

import sys
from collections import defaultdict
from contextlib import contextmanager
from time import monotonic

from typing import Dict, Iterator, List, Set, Tuple


SAMPLE_INPUT = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


# === Part 1 ===

Grid = List[List[int]]
Point = Tuple[int, int]
Path = List[Point]

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)
NEIGHBORS = {UP, DOWN, LEFT, RIGHT}


class WeightedGraph:
    def __init__(self, risks: Grid) -> None:
        self.height = len(risks)
        self.width = len(risks[0])
        self.risks = risks
        self.nodes = {(x, y) for x in range(self.width) for y in range(self.height)}
        self.edges = {
            source: {
                (destination, risks[destination[1]][destination[0]])
                for destination in self.neighbors(source)
            }
            for source in self.nodes
        }

    def neighbors(self, point: Point) -> Iterator[Point]:
        x, y = point
        for dx, dy in {LEFT, RIGHT, UP, DOWN}:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= self.width:
                continue
            if ny < 0 or ny >= self.height:
                continue
            if nx == x and ny == y:
                continue
            yield nx, ny

    def total_path_risk(self, path: Path) -> int:
        return sum(self.risks[y][x] for x, y in path[1:])

    def lowest_risk_path(self, source: Point, goal: Point) -> Path:
        # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

        Q: Set[Point] = self.nodes.copy()
        prev: Dict[Point, Point] = {}

        dist: Dict[Point, int] = defaultdict(lambda: sys.maxsize)
        dist[source] = 0

        while Q:
            u = min(Q, key=lambda x: dist[x])
            Q.remove(u)
            for v, risk in self.edges[u]:
                if v in Q:
                    alt = dist[u] + risk
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u

        path: Path = [goal]
        node = goal
        while node in prev:
            node = prev[node]
            path.insert(0, node)
        return path


def test_parsing() -> None:
    risks = parse(SAMPLE_INPUT)
    assert len(risks) == 10
    assert len(risks[0]) == 10


def test_graph():
    graph = WeightedGraph(parse(SAMPLE_INPUT))
    assert len(graph.nodes) == 100
    assert graph.edges[(4, 1)] == {((3, 1), 1), ((4, 0), 7), ((4, 2), 5), ((5, 1), 7)}
    assert graph.lowest_risk_path((0, 0), (9, 9)) == [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 2),
        (4, 2),
        (5, 2),
        (6, 2),
        (6, 3),
        (7, 3),
        (7, 4),
        (8, 4),
        (8, 5),
        (8, 6),
        (8, 7),
        (8, 8),
        (9, 8),
        (9, 9),
    ]


def test_part1() -> None:
    grid = parse(SAMPLE_INPUT)
    assert part1(grid) == 40


def part1(grid: Grid) -> int:
    graph = WeightedGraph(grid)
    path = graph.lowest_risk_path((0, 0), (graph.width - 1, graph.height - 1))
    return graph.total_path_risk(path)


# === Part 2 ===


def test_part2() -> None:
    grid = parse(SAMPLE_INPUT)
    assert part2(grid) == 315


def part2(grid: Grid) -> int:
    return part1(enlarge(grid, 5))


def test_enlarge() -> None:
    grid = parse(SAMPLE_INPUT)

    assert enlarge(grid, 1) == grid

    res = enlarge(grid, 2)
    assert res == parse(
        """\
11637517422274862853
13813736722492484783
21365113283247622439
36949315694715142671
74634171118574528222
13191281372421239248
13599124212461123532
31254216394236532741
12931385212314249632
23119445813422155692
22748628533385973964
24924847833513595894
32476224394358733541
47151426715826253782
85745282229685639333
24212392483532341359
24611235323572234643
42365327415347643852
23142496323425351743
34221556924533266713"""
    )


def enlarge(grid: Grid, times: int) -> Grid:
    height = len(grid)
    width = len(grid[0])
    return [
        [
            (((grid[y % height][x % width] - 1) + xstep + ystep) % 9) + 1
            for xstep in range(times)
            for x in range(width)
        ]
        for ystep in range(times)
        for y in range(height)
    ]


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> Grid:
    return [[int(char) for char in line] for line in text.splitlines()]


if __name__ == "__main__":
    grid = parse(read_input())
    print("Part 1:", part1(grid))
    print("Part 2:", part2(grid))
