import re
from dataclasses import dataclass
from itertools import combinations


@dataclass
class Vector:
    x: int
    y: int
    z: int

    @classmethod
    def parse(cls, text):
        mo = re.match(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", text)
        return cls(x=int(mo.group(1)), y=int(mo.group(2)), z=int(mo.group(3)))


def test_parse_position():
    assert Vector.parse("<x=-2, y=9, z=-5>") == Vector(x=-2, y=9, z=-5)


def parse_input(text):
    return [Vector.parse(line) for line in text.splitlines()]


@dataclass
class Moon:
    position: Vector
    velocity: Vector

    def update_position(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.position.z += self.velocity.z

    @property
    def potential_energy(self):
        return abs(self.position.x) + abs(self.position.y) + abs(self.position.z)

    @property
    def kinetic_energy(self):
        return abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy


def test_total_energy():
    moon = Moon(position=Vector(x=2, y=1, z=-3), velocity=Vector(x=-3, y=-2, z=1))
    assert moon.total_energy == 36


class System:
    def __init__(self, moon_positions):
        self.moons = [
            Moon(position=position, velocity=Vector(0, 0, 0))
            for position in moon_positions
        ]

    def simulate_steps(self, n):
        for _ in range(n):
            self.simulate_step()

    def simulate_step(self):
        self.apply_gravity()
        for moon in self.moons:
            moon.update_position()

    def apply_gravity(self):
        for first, second in combinations(self.moons, 2):
            for axis in {"x", "y", "z"}:
                first_value = getattr(first.position, axis)
                second_value = getattr(second.position, axis)
                if first_value < second_value:
                    setattr(first.velocity, axis, getattr(first.velocity, axis) + 1)
                    setattr(second.velocity, axis, getattr(second.velocity, axis) - 1)
                if second_value < first_value:
                    setattr(second.velocity, axis, getattr(second.velocity, axis) + 1)
                    setattr(first.velocity, axis, getattr(first.velocity, axis) - 1)

    def total_energy(self):
        return sum(moon.total_energy for moon in self.moons)


def part1(moon_positions):
    system = System(moon_positions)
    system.simulate_steps(1000)
    return system.total_energy()


if __name__ == "__main__":
    with open("day12.txt") as file_:
        moon_positions = parse_input(file_.read())
    # logging.basicConfig(level=logging.DEBUG)
    print("Part 1:", part1(moon_positions))
