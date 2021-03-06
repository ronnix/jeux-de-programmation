#!/usr/bin/env python
import sys

import pytest


TEST_INPUT = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


def test_build_tree():
    assert Node.from_string(TEST_INPUT) == Node(
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
    def from_string(cls, text):
        return cls.from_numbers([int(s) for s in text.split()])

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
        length = index + nb_metadata
        node.metadata = numbers[index:length]
        return node, length

    def sum_metadata(self):
        return sum(self.metadata) + sum(child.sum_metadata() for child in self.children)

    def value(self):
        if not self.children:
            return sum(self.metadata)
        return sum(
            self.children[index - 1].value()
            for index in self.metadata
            if 0 < index <= len(self.children)
        )


def test_sum_metadata():
    assert Node.from_string(TEST_INPUT).sum_metadata() == 138


@pytest.mark.parametrize(
    "tree, value",
    [
        (Node(metadata=[10, 11, 12]), 33),
        (Node(children=[Node(metadata=[99])], metadata=[2]), 0),
        (Node.from_string(TEST_INPUT), 66),
    ],
)
def test_node_value(tree, value):
    assert tree.value() == value


def main():
    tree = Node.from_string(sys.stdin.read())
    print(tree.sum_metadata())
    print(tree.value())


if __name__ == "__main__":
    main()
