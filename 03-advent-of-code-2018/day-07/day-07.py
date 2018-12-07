#!/usr/bin/env python
import sys
from collections import defaultdict


TEST_INPUT = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""


def test_read_input():
    assert read_input(TEST_INPUT.splitlines()) == {
        "A": {"C"},
        "B": {"A"},
        "C": set(),
        "D": {"A"},
        "E": {"B", "D", "F"},
        "F": {"C"},
    }


def read_input(stream):
    dependency_graph = defaultdict(set)
    for line in stream:
        step = line[36]
        required = line[5]
        dependency_graph[step].add(required)
        dependency_graph[required]  # touch this key so that it exists
    return dependency_graph


def test_walk_graph():
    dependency_graph = read_input(TEST_INPUT.splitlines())
    assert walk_graph(dependency_graph) == "CABDFE"


def walk_graph(dependency_graph):
    completed = ""
    remaining = dependency_graph.copy()
    while remaining:
        step = min(
            step
            for step, required in remaining.items()
            if all(dep in completed for dep in required)
        )
        completed += step
        del remaining[step]
    return completed


def main():
    dependency_graph = read_input(sys.stdin)
    print(walk_graph(dependency_graph))


if __name__ == "__main__":
    main()
