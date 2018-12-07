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


def test_step_time():
    assert step_time("A") == 61
    assert step_time("Z") == 86

    assert step_time("A", base_time=0) == 1
    assert step_time("Z", base_time=0) == 26


def step_time(step, base_time=60):
    return base_time + ord(step) - ord("A") + 1


def test_required_time():
    dependency_graph = read_input(TEST_INPUT.splitlines())
    print(dependency_graph)
    assert required_time(dependency_graph, workers=2, base_time=0) == 15


def required_time(dependency_graph, workers, base_time):
    time = -1
    completed = ""
    available_workers = workers
    schedule = defaultdict(list)
    remaining = dependency_graph.copy()

    while remaining or schedule:

        # Move time forward
        time += 1

        # Have any started steps been completed?
        for step in schedule[time]:
            completed += step
            available_workers += 1
        del schedule[time]

        # Can we start a new step?
        while available_workers:
            ready = [
                step
                for step, required in remaining.items()
                if all(dep in completed for dep in required)
            ]
            if ready:
                step = min(ready)
                print(f"Starting step {step} at time {time}")
                available_workers -= 1
                del remaining[step]
                schedule[time + step_time(step, base_time)].append(step)
            else:
                break

    return time


def main():
    dependency_graph = read_input(sys.stdin)
    print(walk_graph(dependency_graph))
    print(required_time(dependency_graph, workers=5, base_time=60))


if __name__ == "__main__":
    main()
