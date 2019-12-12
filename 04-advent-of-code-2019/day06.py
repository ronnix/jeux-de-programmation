from more_itertools import flatten, ilen


def test_total_number_of_orbits():
    orbit_map = parse_orbit_map([
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
    ])
    assert total_number_of_orbits(orbit_map) == 42


def total_number_of_orbits(orbit_map):
    orbits = direct_and_indirect_orbits(orbit_map)
    return ilen(flatten(orbits.values()))


def direct_and_indirect_orbits(orbit_map):
    def _indirect_orbits(obj):
        orbited = orbit_map.get(obj)
        if orbited is None:
            return set()
        return {orbited} | _indirect_orbits(orbited)
    return {obj: _indirect_orbits(obj) for obj in orbit_map}


def read_input():
    with open("day06.txt") as file_:
        return file_.read().splitlines()


def parse_orbit_map(lines):
    return dict(reversed(line.split(")")) for line in lines)


if __name__ == "__main__":
    orbit_map = parse_orbit_map(read_input())
    print("Part 1:", total_number_of_orbits(orbit_map))
