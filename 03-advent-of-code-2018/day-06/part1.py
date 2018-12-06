#!/usr/bin/env python
import sys


def test_read_input():
    res = read_input(["183, 157\n", "331, 86\n"])
    assert list(res) == [(183, 157), (331, 86)]


def read_input(stream):
    return (tuple(map(int, line.strip().split(", "))) for line in stream)


def test_manhattan_distance():
    assert manhattan_distance((0, 0), (0, 0)) == 0
    assert manhattan_distance((0, 0), (1, 1)) == 2
    assert manhattan_distance((1, 1), (0, 0)) == 2
    assert manhattan_distance((5, 0), (1, 1)) == 5
    assert manhattan_distance((5, 0), (5, 5)) == 5
    assert manhattan_distance((5, 0), (8, 3)) == 6


def manhattan_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def test_grid_size():
    assert grid_size([(183, 157), (331, 86)]) == (331, 157)


def grid_size(points):
    return max(p[0] for p in points), max(p[1] for p in points)


def test_closest_locations():
    locations = [
        (1, 1),  # A
        (1, 6),  # B
        (8, 3),  # C
        (3, 4),  # D
        (5, 5),  # E
        (8, 9),  # F
    ]
    assert closest_locations(locations, (0, 0)) == {(1, 1)}
    assert closest_locations(locations, (4, 0)) == {(1, 1)}
    assert closest_locations(locations, (5, 0)) == {(1, 1), (5, 5)}
    assert closest_locations(locations, (6, 0)) == {(8, 3)}


def closest_locations(locations, coordinates):
    distances = {
        location: manhattan_distance(coordinates, location) for location in locations
    }
    shortest = min(distances.values())
    return {
        location for location, distance in distances.items() if distance == shortest
    }


def main():
    print(list(read_input(sys.stdin)))


if __name__ == "__main__":
    main()
