# https://adventofcode.com/2022/day/11

from collections import Counter, deque
from functools import reduce
from typing import Iterable, List
import logging
import operator
import re

import pytest


EXAMPLE_INPUT = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


# === Part 1 ===


def test_part1():
    assert part1(EXAMPLE_INPUT) == 10605


def product(values: Iterable[int]) -> int:
    return reduce(operator.mul, values, 1)


class Item:
    def __init__(self, worry_level: int):
        self.worry_level = worry_level

    def __repr__(self):
        return f"<Item({self.worry_level})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return False
        return self.worry_level == other.worry_level

    @property
    def worry_level(self) -> int:
        return product(factor**count for factor, count in self._factors.items())

    @worry_level.setter
    def worry_level(self, value: int) -> None:
        self._factors = factorize(value)

    def is_divisible_by(self, divisor: int) -> bool:
        return self._factors[divisor] > 0

    def decrease_worry_level(self) -> None:
        self.worry_level //= 3

    def update_worry_level(self, operator: str, operand: str) -> None:
        if operator == "*":
            if operand == "old":
                operand_value = self.worry_level
            else:
                operand_value = int(operand)
            self.worry_level *= operand_value
        else:
            self.worry_level += int(operand)


def factorize(value: int) -> Counter:
    result: Counter = Counter()
    factor = 2
    while factor <= value:
        if value % factor == 0:
            result[factor] += 1
            value //= factor
        else:
            factor += 1
    return result


@pytest.mark.parametrize(
    "value,factors",
    [
        (1, {}),
        (2, {2: 1}),
        (4, {2: 2}),
        (10, {2: 1, 5: 1}),
        (1501, {19: 1, 79: 1}),
        (60, {2: 2, 3: 1, 5: 1}),
        (500, {2: 2, 5: 3}),
    ],
)
def test_factorize(value, factors):
    assert factorize(value) == Counter(factors)


@pytest.mark.parametrize(
    "value",
    [
        60,
        500,
    ],
)
def test_item(value):
    assert Item(value).worry_level == value


def part1(text: str) -> int:
    monkeys = [
        Monkey.from_string(paragraph) for paragraph in text.split("\n\n") if paragraph
    ]
    return level_of_monkey_business(monkeys, rounds=20)


class Monkey:
    def __init__(
        self,
        number: int,
        items: List[Item],
        operator: str,
        operand: str,
        divisor: int,
        dest_if_true: int,
        dest_if_false: int,
    ):
        self.number = number
        self.items = deque(items)
        self.operator = operator
        self.operand = operand
        self.divisor = divisor
        self.dest_if_true = dest_if_true
        self.dest_if_false = dest_if_false

    @classmethod
    def from_string(cls, s):
        mo = re.search(r"Monkey (?P<number>\d+):", s)
        number = int(mo.group("number"))

        mo = re.search(r"Starting items: (?P<items>.+?)\n", s)
        items = [Item(int(item)) for item in mo.group("items").split(", ")]

        mo = re.search(r"Operation: new = old (?P<operator>[\+\*]) (?P<operand>old|\d+)\n", s)
        operator = mo.group("operator")
        operand = mo.group("operand")

        mo = re.search(r"Test: divisible by (?P<divisor>.+?)\n", s)
        divisor = int(mo.group("divisor"))

        mo = re.search(r"  If true: throw to monkey (?P<dest_if_true>.+?)\n", s)
        dest_if_true = int(mo.group("dest_if_true"))

        mo = re.search(r"  If false: throw to monkey (?P<dest_if_false>.+?)$", s)
        dest_if_false = int(mo.group("dest_if_false"))

        return cls(
            number=number,
            items=items,
            operator=operator,
            operand=operand,
            divisor=divisor,
            dest_if_true=dest_if_true,
            dest_if_false=dest_if_false,
        )


def test_parse_monkey():
    from textwrap import dedent

    s = dedent(
        """
        Monkey 0:
          Starting items: 79, 98
          Operation: new = old * 19
          Test: divisible by 23
            If true: throw to monkey 2
            If false: throw to monkey 3
        """
    )
    monkey = Monkey.from_string(s)
    assert monkey.number == 0
    assert monkey.items == deque([Item(79), Item(98)])
    assert monkey.operator == "*"
    assert monkey.operand == "19"
    assert monkey.divisor == 23
    assert monkey.dest_if_true == 2
    assert monkey.dest_if_false == 3


def level_of_monkey_business(monkeys, rounds):
    counts = total_number_of_times_each_monkey_inspects_items(monkeys, rounds)
    (_, n1), (_, n2) = counts.most_common(2)
    return n1 * n2


def total_number_of_times_each_monkey_inspects_items(
    monkeys: List[Monkey], rounds: int
):
    counter: Counter = Counter()
    for round in range(rounds):
        logging.debug(f"Round {round + 1}")
        for monkey in monkeys:
            logging.debug(f"Monkey {monkey.number}")
            while monkey.items:
                counter[monkey.number] += 1
                item = monkey.items.popleft()
                logging.debug(
                    f"  Monkey inspects an item with a worry level of {item}."
                )
                item.update_worry_level(monkey.operator, monkey.operand)
                logging.debug(f"    Worry level is {monkey.operator} {monkey.operand} to {item}.")
                item.decrease_worry_level()
                logging.debug(
                    f"    Monkey gets bored with item. Worry level is divided by 3 to {item}."
                )
                divisible = item.is_divisible_by(monkey.divisor)
                logging.debug(
                    f"    Current worry level {'is' if divisible else 'is not'} divisible by {monkey.divisor}."
                )
                dest = monkey.dest_if_true if divisible else monkey.dest_if_false
                monkeys[dest].items.append(item)
                logging.debug(
                    f"    Item with worry level {item} is thrown to monkey {dest}."
                )
        for monkey in monkeys:
            logging.debug(
                f"Monkey {monkey.number}: {', '.join(map(str, monkey.items))}"
            )
    return counter


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
