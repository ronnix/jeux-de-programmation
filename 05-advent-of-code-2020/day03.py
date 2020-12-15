from textwrap import dedent

import pytest


class TreeMap:
    def __init__(self, text):
        self.lines = text.splitlines()

    def at(self, x, y):
        return self.lines[y][x % len(self.lines[0])]

    @property
    def height(self):
        return len(self.lines)

    def count_trees(self, slope_x, slope_y):
        x, y = 0, 0
        assert self.at(x, y) == "."  # start on open square

        trees = 0
        while y < self.height:
            trees += 1 if self.at(x, y) == "#" else 0
            x += slope_x
            y += slope_y
        return trees


@pytest.fixture
def sample_tree_map():
    return TreeMap(
        dedent(
            """\
            ..##.......
            #...#...#..
            .#....#..#.
            ..#.#...#.#
            .#...##..#.
            ..#.##.....
            .#.#.#....#
            .#........#
            #.##...#...
            #...##....#
            .#..#...#.#
            """
        )
    )


class TestTreeMap:
    def test_at(self, sample_tree_map):
        assert sample_tree_map.at(0, 0) == "."
        assert sample_tree_map.at(2, 0) == "#"
        assert sample_tree_map.at(13, 0) == "#"
        assert sample_tree_map.at(0, 1) == "#"

    def test_height(self, sample_tree_map):
        assert sample_tree_map.height == 11

    def test_count_trees(self, sample_tree_map):
        assert sample_tree_map.count_trees(3, 1) == 7


if __name__ == "__main__":
    with open("day03.txt") as f:
        tree_map = TreeMap(f.read())
    print("Part 1:", tree_map.count_trees(3, 1))
