#!/usr/bin/env python
import sys


TEST_INPUT = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


def test_parse_input():
    assert parse_input(TEST_INPUT) == [
        2,
        3,
        0,
        3,
        10,
        11,
        12,
        1,
        1,
        0,
        1,
        99,
        2,
        1,
        1,
        2,
    ]


def parse_input(text):
    return [int(s) for s in text.split()]


def test_build_tree():
    assert Node.from_numbers(parse_input(TEST_INPUT)) == Node(
        children=[
            Node(metadata=[10, 11, 12]),
            Node(children=[Node(metadata=[99])], metadata=[2]),
        ],
        metadata=[1, 1, 2],
    )


class Node:
    def __init__(self, children=None, metadata=None):
        self.children = children if children is not None else []
        self.metadata = metadata if metadata is not None else []

    def __repr__(self):
        return f"Node(children={self.children!r}, metadata={self.metadata!r}"

    def __eq__(self, other):
        return self.children == other.children and self.metadata == other.metadata

    @classmethod
    def from_numbers(cls, numbers):
        return cls._from_numbers(numbers)[0]

    @classmethod
    def _from_numbers(cls, numbers):
        node = cls()
        nb_children = numbers[0]
        nb_metadata = numbers[1]
        index = 2
        for _ in range(nb_children):
            child, length = cls._from_numbers(numbers[index:])
            node.children.append(child)
            index += length
        node.metadata = numbers[index : index + nb_metadata]
        return node, index + nb_metadata


def main():
    numbers = parse_input(sys.stdin.read())
    tree = Node.from_numbers(numbers)
    print(tree)


if __name__ == "__main__":
    main()
