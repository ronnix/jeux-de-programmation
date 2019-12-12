from more_itertools import flatten, ilen


def test_total_number_of_orbits():
    orbit_map = parse_orbit_map(
        ["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L",]
    )
    assert total_number_of_orbits(orbit_map) == 42


def total_number_of_orbits(orbit_map):
    orbits = direct_and_indirect_orbits(orbit_map)
    return ilen(flatten(orbits.values()))


def direct_and_indirect_orbits(orbit_map):
    def _indirect_orbits(obj):
        orbited = orbit_map.get(obj)
        if orbited is None:
            return []
        return _indirect_orbits(orbited) + [orbited]

    return {obj: _indirect_orbits(obj) for obj in orbit_map}


def number_of_orbit_transfers(src, dst, orbit_map):
    orbits = direct_and_indirect_orbits(orbit_map)
    pivot = common_parent(orbits[src], orbits[dst])
    return distance(src, pivot, orbit_map) + distance(dst, pivot, orbit_map)


def common_parent(parents1, parents2):
    common = None
    for p1, p2 in zip(parents1, parents2):
        if p1 != p2:
            break
        common = p1
    return common


def distance(outer, inner, orbit_map):
    if outer == inner:
        return 0
    return 1 + distance(orbit_map[outer], inner, orbit_map)


def read_input():
    with open("day06.txt") as file_:
        return file_.read().splitlines()


def parse_orbit_map(lines):
    return dict(reversed(line.split(")")) for line in lines)


if __name__ == "__main__":
    orbit_map = parse_orbit_map(read_input())
    print("Part 1:", total_number_of_orbits(orbit_map))
    print(
        f"Part 2:",
        number_of_orbit_transfers(orbit_map["YOU"], orbit_map["SAN"], orbit_map),
    )
