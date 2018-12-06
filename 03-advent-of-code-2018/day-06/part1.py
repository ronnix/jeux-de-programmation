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


def test_has_infinite_area():
    locations = [
        (1, 1),  # A
        (1, 6),  # B
        (8, 3),  # C
        (3, 4),  # D
        (5, 5),  # E
        (8, 9),  # F
    ]
    assert has_infinite_area(locations, (1, 1))  # A
    assert has_infinite_area(locations, (1, 6))  # B
    assert has_infinite_area(locations, (8, 3))  # C
    assert not has_infinite_area(locations, (3, 4))  # D
    assert not has_infinite_area(locations, (5, 5))  # E
    assert has_infinite_area(locations, (8, 9))  # F


def has_infinite_area(locations, location):
    """
    If we go in any one of the 4 directions, and for all the coordinates
    we find until we reach the edge of the grid, the location is the closest
    one, then it has in infinite area.
    """
    x_min, y_min = 0, 0
    x_max, y_max = grid_size(locations)
    x_loc, y_loc = location

    up = ((x_loc, y) for y in range(y_min, max(y_min, y_loc)))
    down = ((x_loc, y) for y in range(min(y_max, y_loc + 1), y_max + 1))
    left = ((x, y_loc) for x in range(x_min, max(x_min, x_loc)))
    right = ((x, y_loc) for x in range(min(x_max, x_loc + 1), x_max + 1))

    return any(
        all(
            closest_locations(locations, point) == {location}
            for point in axis
        )
        for axis in (up, down, left, right)
    )


def main():
    print(list(read_input(sys.stdin)))


if __name__ == "__main__":
    main()
