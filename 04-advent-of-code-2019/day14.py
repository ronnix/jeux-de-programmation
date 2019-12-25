import logging
import math
from collections import Counter
from textwrap import dedent

logger = logging.getLogger(__name__)


def parse_input(data):
    return {
        output: (quantity, inputs)
        for output, quantity, inputs in (parse_line(line) for line in data.splitlines())
    }


def parse_line(line):
    left, right = line.split(" => ")
    inputs = [parse_chemical(input_) for input_ in left.split(", ")]
    quantity, output = parse_chemical(right)
    return output, quantity, inputs


def parse_chemical(s):
    quantity, symbol = s.split(" ")
    return int(quantity), symbol


class NanoFactory:
    def __init__(self, reactions):
        self.reactions = reactions
        self.stock = Counter()

    def make(self, chemical, quantity):
        if chemical == "ORE":
            logger.debug("Requiring %d ORE", quantity)
            return quantity
        logger.debug("Trying to make %d %s", quantity, chemical)
        from_stock = min(quantity, self.stock[chemical])
        if from_stock > 0:
            logger.debug("Taking %d already in stock", from_stock)
            self.stock[chemical] -= from_stock
            quantity -= from_stock
        n, inputs = self.reactions[chemical]
        ratio = math.ceil(quantity / n)
        logger.debug("Running reaction %d times", ratio)
        required_ore = sum(
            self.make(input_chemical, ratio * input_quantity)
            for input_quantity, input_chemical in inputs
        )
        extra = (n * ratio) - quantity
        if extra:
            self.stock[chemical] += extra
            logger.debug("Adding %d %s to stock", extra, chemical)
        return required_ore


def test_required_ore():
    factory = NanoFactory(
        parse_input(
            dedent(
                """\
            10 ORE => 10 A
            1 ORE => 1 B
            7 A, 1 B => 1 C
            7 A, 1 C => 1 D
            7 A, 1 D => 1 E
            7 A, 1 E => 1 FUEL
            """
            )
        )
    )
    required_ore = factory.make("FUEL", 1)
    assert required_ore == 31


def part1(reactions):
    factory = NanoFactory(reactions)
    required_ore = factory.make("FUEL", 1)
    return required_ore


if __name__ == "__main__":
    with open("day14.txt") as file_:
        reactions = parse_input(file_.read())
    # logging.basicConfig(level=logging.DEBUG)
    print("Part 1:", part1(reactions))
