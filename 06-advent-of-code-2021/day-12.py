# https://adventofcode.com/2021/day/12

from typing import Iterator, List, FrozenSet


SAMPLE_INPUT = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end"""


# === Part 1 ===

Node = str
Edge = FrozenSet[Node]
Path = List[Node]


class Graph:
    def __init__(self, edges: FrozenSet[Edge]):
        self.edges = edges

    def paths(self, start="start", end="end") -> Iterator[Path]:
        return self._paths(path=[start], end=end)

    def _paths(self, path: Path, end: Node) -> Iterator[Path]:
        last = path[-1]
        if last == end:
            yield path
        else:
            for succ in self.successors(last):
                if succ.islower() and succ in path:  # visit small caves only once
                    continue
                yield from self._paths(path + [succ], end=end)

    def successors(self, node: Node) -> Iterator[Node]:
        for edge in self.edges:
            if node in edge:
                yield set(edge - {node}).pop()


def test_paths() -> None:
    graph = parse(SAMPLE_INPUT)
    assert set(tuple(path) for path in graph.paths()) == {
        ("start", "A", "b", "A", "c", "A", "end"),
        ("start", "A", "b", "A", "end"),
        ("start", "A", "b", "end"),
        ("start", "A", "c", "A", "b", "A", "end"),
        ("start", "A", "c", "A", "b", "end"),
        ("start", "A", "c", "A", "end"),
        ("start", "A", "end"),
        ("start", "b", "A", "c", "A", "end"),
        ("start", "b", "A", "end"),
        ("start", "b", "end"),
    }


def part1(graph: Graph) -> int:
    return len(list(graph.paths()))


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> Graph:
    edges = frozenset(frozenset(line.split("-", 1)) for line in text.splitlines())
    return Graph(edges)


if __name__ == "__main__":
    print("Part 1:", part1(parse(read_input())))
