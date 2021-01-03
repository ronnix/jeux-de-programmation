from collections import Counter
from functools import lru_cache
from textwrap import dedent

from more_itertools import windowed

import pytest


@pytest.fixture
def sample_adapters():
    return parse_input(
        dedent(
            """\
            16
            10
            15
            5
            1
            11
            7
            19
            6
            12
            4
            """
        )
    )


@pytest.fixture
def larger_example():
    return parse_input(
        dedent(
            """\
            28
            33
            18
            42
            31
            14
            46
            20
            48
            47
            24
            23
            49
            45
            19
            38
            39
            11
            1
            32
            25
            35
            8
            17
            7
            9
            4
            2
            34
            10
            3
            """
        )
    )


def parse_input(text):
    return {int(line) for line in text.splitlines()}


def test_device_joltage(sample_adapters):
    assert device_joltage(sample_adapters) == 22


def device_joltage(adapters):
    return max(adapters) + 3


def test_chain_of_adapters(sample_adapters):
    n1, n3 = differences(
        chain_of_adapters(sample_adapters | {0, device_joltage(sample_adapters)})
    )
    assert (n1, n3) == (7, 5)


def test_larger_example(larger_example):
    n1, n3 = differences(
        chain_of_adapters(larger_example | {0, device_joltage(larger_example)})
    )
    assert (n1, n3) == (22, 10)


def chain_of_adapters(adapters):
    return sorted(adapters)


def differences(chain):
    differences = Counter(
        next_adapter - adapter
        for adapter, next_adapter in windowed(chain, 2)
        if next_adapter is not None
    )
    return differences[1], differences[3]


def part1(adapters):
    n1, n3 = differences(chain_of_adapters(adapters | {0, device_joltage(adapters)}))
    return n1 * n3


def test_arrangements(sample_adapters):
    assert arrangements(sample_adapters) == {
        (0, 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, 22),
        (0, 1, 4, 5, 6, 7, 10, 12, 15, 16, 19, 22),
        (0, 1, 4, 5, 7, 10, 11, 12, 15, 16, 19, 22),
        (0, 1, 4, 5, 7, 10, 12, 15, 16, 19, 22),
        (0, 1, 4, 6, 7, 10, 11, 12, 15, 16, 19, 22),
        (0, 1, 4, 6, 7, 10, 12, 15, 16, 19, 22),
        (0, 1, 4, 7, 10, 11, 12, 15, 16, 19, 22),
        (0, 1, 4, 7, 10, 12, 15, 16, 19, 22),
    }


def test_larger_arrangements(larger_example):
    assert len(arrangements(larger_example)) == 19208


def arrangements(adapters):
    last = device_joltage(adapters)

    def _arrangements(sequence):
        previous = sequence[-1]
        for adapter in adapters:
            if 1 <= adapter - previous <= 3:
                yield from _arrangements(sequence + [adapter])
        if 1 <= last - previous <= 3:
            yield sequence + [last]

    return {tuple(a) for a in _arrangements([0])}


def test_efficiently_count_arrangements(sample_adapters):
    assert efficiently_count_arrangements(sample_adapters) == 8


def test_efficiently_count_larger_arrangements(larger_example):
    assert efficiently_count_arrangements(larger_example) == 19208


def efficiently_count_arrangements(adapters):
    start = 0
    end = device_joltage(adapters)
    nodes = sorted(adapters | {start, end})

    @lru_cache
    def nb_paths(origin, destination):
        if origin == destination:
            return 1
        successors = {node for node in nodes if 1 <= node - origin <= 3}
        return sum(nb_paths(node, destination) for node in successors)

    return nb_paths(start, end)


def part2(adapters):
    return efficiently_count_arrangements(adapters)


if __name__ == "__main__":
    with open("day10.txt") as f:
        adapters = parse_input(f.read())
    print("Part 1:", part1(adapters))
    print("Part 2:", part2(adapters))
