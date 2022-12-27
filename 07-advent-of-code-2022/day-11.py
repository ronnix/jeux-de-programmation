# https://adventofcode.com/2022/day/11

from collections import Counter, deque
from typing import List
import logging
import re


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
        return self._worry_level

    @worry_level.setter
    def worry_level(self, value: int) -> None:
        self._worry_level = value

    def is_divisible_by(self, divisor: int) -> bool:
        return (self._worry_level % divisor) == 0

    def update_worry_level(self, operation: str) -> None:
        mo = re.match(r"old (?P<op>[\*\+]) (?P<operand>old|\d+)", operation)
        assert mo is not None
        if mo.group("op") == "*":
            if mo.group("operand") == "old":
                operand = self.worry_level
            else:
                operand = int(mo.group("operand"))
            self.worry_level *= operand
        else:
            self.worry_level += int(mo.group("operand"))


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
        operation: str,
        divisor: int,
        dest_if_true: int,
        dest_if_false: int,
    ):
        self.number = number
        self.items = deque(items)
        self.operation = operation
        self.divisor = divisor
        self.dest_if_true = dest_if_true
        self.dest_if_false = dest_if_false

    @classmethod
    def from_string(cls, s):
        mo = re.search(r"Monkey (?P<number>\d+):", s)
        number = int(mo.group("number"))

        mo = re.search(r"Starting items: (?P<items>.+?)\n", s)
        items = [Item(int(item)) for item in mo.group("items").split(", ")]

        mo = re.search(r"Operation: new = (?P<operation>.+?)\n", s)
        operation = mo.group("operation")

        mo = re.search(r"Test: divisible by (?P<divisor>.+?)\n", s)
        divisor = int(mo.group("divisor"))

        mo = re.search(r"  If true: throw to monkey (?P<dest_if_true>.+?)\n", s)
        dest_if_true = int(mo.group("dest_if_true"))

        mo = re.search(r"  If false: throw to monkey (?P<dest_if_false>.+?)$", s)
        dest_if_false = int(mo.group("dest_if_false"))

        return cls(
            number=number,
            items=items,
            operation=operation,
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
    assert monkey.operation == "old * 19"
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
                item.update_worry_level(monkey.operation)
                logging.debug(f"    Worry level is {monkey.operation} to {item}.")
                item.worry_level //= 3
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
