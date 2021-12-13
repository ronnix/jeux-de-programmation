# https://adventofcode.com/2021/day/12

from collections import Counter
from typing import Callable, Iterator, List, FrozenSet


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

    def paths(self, is_valid: Callable[[Path], bool]) -> Iterator[Path]:
        return self._paths(path=["start"], end="end", is_valid=is_valid)

    def _paths(
        self, path: Path, end: Node, is_valid: Callable[[Path], bool]
    ) -> Iterator[Path]:
        last = path[-1]
        if last == end:
            yield path
        else:
            for succ in self.successors(last):
                expanded_path = path + [succ]
                if is_valid(expanded_path):
                    yield from self._paths(expanded_path, end=end, is_valid=is_valid)

    def successors(self, node: Node) -> Iterator[Node]:
        for edge in self.edges:
            if node in edge:
                yield set(edge - {node}).pop()


def is_valid_part1(path: Path):
    counts = Counter(cave for cave in path if cave.islower())
    return set(counts.values()) == {1}


def test_paths_part1() -> None:
    graph = parse(SAMPLE_INPUT)
    assert set(tuple(path) for path in graph.paths(is_valid_part1)) == {
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
    return len(list(graph.paths(is_valid_part1)))


# === Part 2 ===


def is_valid_part2(path: Path):
    counts = Counter(cave for cave in path if cave.islower())
    if counts.pop("start") > 1:
        return False
    if "end" in counts and counts.pop("end") > 1:
        return False
    if any(count > 2 for count in counts.values()):
        return False
    if Counter(counts.values())[2] > 1:
        return False
    return True


def test_paths_part2() -> None:
    graph = parse(SAMPLE_INPUT)
    assert set(tuple(path) for path in graph.paths(is_valid_part2)) == {
        ("start", "A", "b", "A", "b", "A", "c", "A", "end"),
        ("start", "A", "b", "A", "b", "A", "end"),
        ("start", "A", "b", "A", "b", "end"),
        ("start", "A", "b", "A", "c", "A", "b", "A", "end"),
        ("start", "A", "b", "A", "c", "A", "b", "end"),
        ("start", "A", "b", "A", "c", "A", "c", "A", "end"),
        ("start", "A", "b", "A", "c", "A", "end"),
        ("start", "A", "b", "A", "end"),
        ("start", "A", "b", "d", "b", "A", "c", "A", "end"),
        ("start", "A", "b", "d", "b", "A", "end"),
        ("start", "A", "b", "d", "b", "end"),
        ("start", "A", "b", "end"),
        ("start", "A", "c", "A", "b", "A", "b", "A", "end"),
        ("start", "A", "c", "A", "b", "A", "b", "end"),
        ("start", "A", "c", "A", "b", "A", "c", "A", "end"),
        ("start", "A", "c", "A", "b", "A", "end"),
        ("start", "A", "c", "A", "b", "d", "b", "A", "end"),
        ("start", "A", "c", "A", "b", "d", "b", "end"),
        ("start", "A", "c", "A", "b", "end"),
        ("start", "A", "c", "A", "c", "A", "b", "A", "end"),
        ("start", "A", "c", "A", "c", "A", "b", "end"),
        ("start", "A", "c", "A", "c", "A", "end"),
        ("start", "A", "c", "A", "end"),
        ("start", "A", "end"),
        ("start", "b", "A", "b", "A", "c", "A", "end"),
        ("start", "b", "A", "b", "A", "end"),
        ("start", "b", "A", "b", "end"),
        ("start", "b", "A", "c", "A", "b", "A", "end"),
        ("start", "b", "A", "c", "A", "b", "end"),
        ("start", "b", "A", "c", "A", "c", "A", "end"),
        ("start", "b", "A", "c", "A", "end"),
        ("start", "b", "A", "end"),
        ("start", "b", "d", "b", "A", "c", "A", "end"),
        ("start", "b", "d", "b", "A", "end"),
        ("start", "b", "d", "b", "end"),
        ("start", "b", "end"),
    }


def part2(graph: Graph) -> int:
    return len(list(graph.paths(is_valid_part2)))


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> Graph:
    edges = frozenset(frozenset(line.split("-", 1)) for line in text.splitlines())
    return Graph(edges)


if __name__ == "__main__":
    print("Part 1:", part1(parse(read_input())))
    print("Part 2:", part2(parse(read_input())))
