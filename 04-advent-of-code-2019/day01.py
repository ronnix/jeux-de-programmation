import pytest


@pytest.mark.parametrize("mass, fuel", [
    (12, 2),
    (14, 2),
    (1969, 654),
    (100756, 33583),
    (2, 0),
])
def test_required_fuel(mass, fuel):
    assert required_fuel(mass) == fuel


def required_fuel(mass):
    return max(0, mass // 3 - 2)


def part1(values):
    return sum(required_fuel(mass) for mass in values)


@pytest.mark.parametrize("mass, fuel", [
    (14, 2),
    (1969, 966),
    (100756, 50346),
])
def test_required_fuel_taking_fuel_mass_into_account(mass, fuel):
    assert required_fuel_taking_fuel_mass_into_account(mass) == fuel


def required_fuel_taking_fuel_mass_into_account(mass):
    extra_mass = []
    while True:
        mass = required_fuel(mass)
        if mass == 0:
            break
        extra_mass.append(mass)
    return sum(extra_mass)


def part2(values):
    return sum(required_fuel_taking_fuel_mass_into_account(mass) for mass in values)


if __name__ == '__main__':
    with open("day01.txt") as file_:
        values = [int(line) for line in file_]
    print("Part 1:", part1(values))
    print("Part 2:", part2(values))
