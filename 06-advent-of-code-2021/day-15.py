# https://adventofcode.com/2021/day/15

from collections import defaultdict

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
            (source, destination): risks[destination[1]][destination[0]]
            for source in self.nodes
            for destination in self.neighbors(source)
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

        dist: Dict[Point, int] = defaultdict(lambda: 99999999)
        dist[source] = 0

        while Q:
            u = sorted(Q, key=lambda x: dist[x])[0]
            Q -= {u}
            for v in self.neighbors(u):
                if v in Q:
                    alt = dist[u] + self.edges[(u, v)]
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
    assert graph.edges[(4, 1), (4, 2)] == 5
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


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> Grid:
    return [[int(char) for char in line] for line in text.splitlines()]


if __name__ == "__main__":
    grid = parse(read_input())
    print("Part 1:", part1(grid))
