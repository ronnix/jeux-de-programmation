#!/usr/bin/env python
from dataclasses import dataclass
from itertools import cycle

import pytest


DATA = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """


def test_read_input():
    world = World(DATA)
    assert world[2, 0] == "-"
    assert world[9, 3] == "|"
    assert world.carts == [Cart(2, 0, ">", "left"), Cart(9, 3, "v", "left")]


def test_str():
    world = World(DATA)
    assert str(world) == r"""/---\        
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/   """


NEXT_TURN = {
    "left": "straight",
    "straight": "right",
    "right": "left",
}


class Collision(Exception):
    def __init__(self, x, y):
        self.x = x
        self.y = y


@dataclass
class Cart:
    x: int
    y: int
    direction: str
    next_turn: str = "left"

    def next(self, world):
        next_x, next_y, next_direction = self.x, self.y, self.direction
        # print(f"\nCurrent cart: {self.x}, {self.y}, {self.direction}")
        if self.direction == "v":
            next_y += 1
        if self.direction == "^":
            next_y -= 1
        if self.direction == "<":
            next_x -= 1
        if self.direction == ">":
            next_x += 1
        next_cell = world[next_x, next_y]
        # print(f"Next cell: {next_x}, {next_y}, {next_cell!r}")
        if next_cell == "/":
            if self.direction == "^":
                next_direction = ">"
            if self.direction == "v":
                next_direction = "<"
            if self.direction == "<":
                next_direction = "v"
            if self.direction == ">":
                next_direction = "^"
            # print(f"{self.direction} -> {next_direction}")
        if next_cell == "\\":
            if self.direction == "^":
                next_direction = "<"
            if self.direction == "v":
                next_direction = ">"
            if self.direction == "<":
                next_direction = "^"
            if self.direction == ">":
                next_direction = "v"
            # print(f"{self.direction} -> {next_direction}")
        if next_cell == "+":
            turn = self.next_turn
            self.next_turn = NEXT_TURN[self.next_turn]
            if turn == "left":
                if self.direction == "^":
                    next_direction = "<"
                if self.direction == "v":
                    next_direction = ">"
                if self.direction == "<":
                    next_direction = "v"
                if self.direction == ">":
                    next_direction = "^"
            if turn == "right":
                if self.direction == "^":
                    next_direction = ">"
                if self.direction == "v":
                    next_direction = "<"
                if self.direction == "<":
                    next_direction = "^"
                if self.direction == ">":
                    next_direction = "v"
            if turn == "straight":
                next_direction = self.direction
            # print(f"{id(self)} Turning {turn}: {self.direction} -> {next_direction}")
        if any(cart.x == next_x and cart.y == next_y for cart in world.carts):
            raise Collision(next_x, next_y)
        self.x = next_x
        self.y = next_y
        self.direction = next_direction
        return self


@pytest.mark.parametrize("ticks,carts", [
    (1, [Cart(3, 0, ">", "left"), Cart(9, 4, ">", "straight")]),
    (2, [Cart(4, 0, "v", "left"), Cart(10, 4, ">", "straight")]),
    (3, [Cart(4, 1, "v", "left"), Cart(11, 4, ">", "straight")]),
    (4, [Cart(4, 2, ">", "straight"), Cart(12, 4, "^", "straight")]),
    (5, [Cart(5, 2, ">", "straight"), Cart(12, 3, "^", "straight")]),
    (6, [Cart(6, 2, ">", "straight"), Cart(12, 2, "^", "straight")]),
    (7, [Cart(7, 2, ">", "right"), Cart(12, 1, "<", "straight")]),
    (8, [Cart(8, 2, ">", "right"), Cart(11, 1, "<", "straight")]),
    (9, [Cart(9, 2, "v", "right"), Cart(10, 1, "<", "straight")]),
    (10, [Cart(9, 3, "v", "right"), Cart(9, 1, "<", "straight")]),
    (11, [Cart(9, 4, "<", "left"), Cart(8, 1, "<", "straight")]),
    (12, [Cart(8, 4, "<", "left"), Cart(7, 1, "v", "straight")]),
    (13, [Cart(7, 4, "^", "left"), Cart(7, 2, "v", "right")]),
])
def test_next_tick(ticks, carts):
    world = World(DATA)
    for _ in range(ticks):
        world.next_tick()
    assert world.carts == carts


def test_collision():
    world = World(DATA)
    for _ in range(13):
        world.next_tick()
    with pytest.raises(Collision):
        world.next_tick()


class World:
    def __init__(self, data):
        self.tracks, self.carts = self.read_input(data)

    def __getitem__(self, coords):
        x, y = coords
        return self.tracks[y][x]

    def __str__(self):
        return "\n".join("".join(line) for line in self.tracks)

    def next_tick(self):
        self.carts = [cart.next(self) for cart in self.carts]

    @staticmethod
    def read_input(input_data):
        lines = []
        carts = []
        for y, chars in enumerate(input_data.splitlines()):
            line = []
            for x, char in enumerate(chars):
                if char == "v":
                    carts.append(Cart(x=x, y=y, direction=char))
                    char = "|"
                if char == "^":
                    carts.append(Cart(x=x, y=y, direction=char))
                    char = "|"
                if char == "<":
                    carts.append(Cart(x=x, y=y, direction=char))
                    char = "-"
                if char == ">":
                    carts.append(Cart(x=x, y=y, direction=char))
                    char = "-"
                line.append(char)
            lines.append(line)
        return lines, carts


def main():
    with open("input.txt") as f:
        world = World(f.read())
    while True:
        try:
            world.next_tick()
        except Collision as collision:
            print(f"{collision.x},{collision.y}")
            break


if __name__ == "__main__":
    main()
