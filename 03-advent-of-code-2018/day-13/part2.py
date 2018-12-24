#!/usr/bin/env python
from dataclasses import dataclass
from itertools import cycle

import pytest


DATA = r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/"""


NEXT_TURN = {"left": "straight", "straight": "right", "right": "left"}


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

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

    def next(self, world):
        next_x, next_y, next_direction = self.x, self.y, self.direction
        if self.direction == "v":
            next_y += 1
        if self.direction == "^":
            next_y -= 1
        if self.direction == "<":
            next_x -= 1
        if self.direction == ">":
            next_x += 1
        next_cell = world[next_x, next_y]
        if next_cell == "/":
            if self.direction == "^":
                next_direction = ">"
            if self.direction == "v":
                next_direction = "<"
            if self.direction == "<":
                next_direction = "v"
            if self.direction == ">":
                next_direction = "^"
        if next_cell == "\\":
            if self.direction == "^":
                next_direction = "<"
            if self.direction == "v":
                next_direction = ">"
            if self.direction == "<":
                next_direction = "^"
            if self.direction == ">":
                next_direction = "v"
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
        if any(cart.x == next_x and cart.y == next_y for cart in world.carts):
            raise Collision(next_x, next_y)
        self.x = next_x
        self.y = next_y
        self.direction = next_direction
        return self


@pytest.mark.parametrize(
    "ticks,carts",
    [
        (
            0,
            [
                Cart(x=1, y=0, direction=">", next_turn="left"),
                Cart(x=3, y=0, direction="<", next_turn="left"),
                Cart(x=3, y=2, direction="<", next_turn="left"),
                Cart(x=6, y=3, direction="v", next_turn="left"),
                Cart(x=1, y=4, direction=">", next_turn="left"),
                Cart(x=3, y=4, direction="<", next_turn="left"),
                Cart(x=6, y=5, direction="^", next_turn="left"),
                Cart(x=3, y=6, direction="<", next_turn="left"),
                Cart(x=5, y=6, direction=">", next_turn="left"),
            ],
        ),
        (
            1,
            [
                Cart(x=2, y=2, direction="v", next_turn="left"),
                Cart(x=2, y=6, direction="^", next_turn="left"),
                Cart(x=6, y=6, direction="^", next_turn="left"),
            ],
        ),
        (
            2,
            [
                Cart(x=2, y=3, direction="v", next_turn="left"),
                Cart(x=2, y=5, direction="^", next_turn="left"),
                Cart(x=6, y=5, direction="^", next_turn="left"),
            ],
        ),
        (3, [Cart(x=6, y=4, direction="^", next_turn="left")]),
    ],
)
def test_next_tick(ticks, carts):
    world = World(DATA)
    for _ in range(ticks):
        assert world.next_tick() is None
    assert world.carts == carts


class World:
    def __init__(self, data):
        self.tracks, self.carts = self.read_input(data)

    def __getitem__(self, coords):
        x, y = coords
        return self.tracks[y][x]

    def __str__(self):
        return "\n".join("".join(line) for line in self.tracks)

    def next_tick(self):
        to_move = sorted(self.carts)
        while to_move:
            current_cart = to_move.pop(0)
            try:
                current_cart.next(self)
            except Collision as collision:
                to_move = [
                    cart
                    for cart in to_move
                    if cart.x != collision.x or cart.y != collision.y
                ]
                self.carts = [
                    cart
                    for cart in self.carts
                    if (cart.x != collision.x or cart.y != collision.y)
                    and cart is not current_cart
                ]

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
    while len(world.carts) > 1:
        world.next_tick()
    print(f"{world.carts[0].x},{world.carts[0].y}")


if __name__ == "__main__":
    main()
