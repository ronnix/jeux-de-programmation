#!/usr/bin/env python
import sys


TEST_LOCATIONS = [
    (1, 1),  # A
    (1, 6),  # B
    (8, 3),  # C
    (3, 4),  # D
    (5, 5),  # E
    (8, 9),  # F
]


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
    assert closest_locations(TEST_LOCATIONS, (0, 0)) == {(1, 1)}
    assert closest_locations(TEST_LOCATIONS, (4, 0)) == {(1, 1)}
    assert closest_locations(TEST_LOCATIONS, (5, 0)) == {(1, 1), (5, 5)}
    assert closest_locations(TEST_LOCATIONS, (6, 0)) == {(8, 3)}


def closest_locations(locations, coordinates):
    distances = {
        location: manhattan_distance(coordinates, location) for location in locations
    }
    shortest = min(distances.values())
    return {
        location for location, distance in distances.items() if distance == shortest
    }


def test_has_infinite_area():
    assert has_infinite_area(TEST_LOCATIONS, (1, 1))  # A
    assert has_infinite_area(TEST_LOCATIONS, (1, 6))  # B
    assert has_infinite_area(TEST_LOCATIONS, (8, 3))  # C
    assert not has_infinite_area(TEST_LOCATIONS, (3, 4))  # D
    assert not has_infinite_area(TEST_LOCATIONS, (5, 5))  # E
    assert has_infinite_area(TEST_LOCATIONS, (8, 9))  # F


def has_infinite_area(locations, location):
    """
    For any of the 4 directions, if the location is the closest to the point
    at the edge of the grid in that direction, then it has in infinite area.
    """
    x_min, y_min = 0, 0
    x_max, y_max = grid_size(locations)
    x_loc, y_loc = location

    up = (x_loc, y_min)
    down = (x_loc, y_max)
    left = (x_min, y_loc)
    right = (x_max, y_loc)

    return any(
        closest_locations(locations, point) == {location}
        for point in (up, down, left, right)
    )


def test_area():
    assert area(TEST_LOCATIONS, (3, 4)) == 9
    assert area(TEST_LOCATIONS, (5, 5)) == 17


def area(locations, location):
    x_loc, y_loc = location
    width, height = grid_size(locations)

    x_min = x_loc
    while x_min > 0:
        if closest_locations(locations, (x_min, y_loc)) != {location}:
            break
        x_min -= 1

    x_max = x_loc
    while x_max < width:
        if closest_locations(locations, (x_max, y_loc)) != {location}:
            break
        x_max += 1

    y_min = y_loc
    while y_min > 0:
        if closest_locations(locations, (x_loc, y_min)) != {location}:
            break
        y_min -= 1

    y_max = y_loc
    while y_max < height:
        if closest_locations(locations, (x_loc, y_max)) != {location}:
            break
        y_max += 1

    return sum(
        int(closest_locations(locations, (x, y)) == {location})
        for x in range(x_min, x_max + 1)
        for y in range(y_min, y_max + 1)
    )


def test_largest_finite_area():
    assert largest_finite_area(TEST_LOCATIONS) == 17


def largest_finite_area(locations):
    return max(
        area(locations, location)
        for location in locations
        if not has_infinite_area(locations, location)
    )


def main():
    locations = list(read_input(sys.stdin))
    size = largest_finite_area(locations)
    print(f"The size of the largest area that isn't infinite is {size}")


if __name__ == "__main__":
    main()
