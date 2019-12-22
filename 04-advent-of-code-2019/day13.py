import logging

from more_itertools import ilen

from intcode import IntcodeComputer


logger = logging.getLogger(__name__)


BLOCK_TILE = 2


class ArcadeCabinet:
    def __init__(self, program):
        self.computer = IntcodeComputer(program)
        self.screen = {}

    def run(self):
        coroutine = self.computer.run()
        try:
            while True:
                x, y, tile = next(coroutine), next(coroutine), next(coroutine)
                logger.debug((x, y, tile))
                self.screen[(x, y)] = tile
        except StopIteration:
            logger.debug("Program terminated")


def part1(program):
    arcade_cabinet = ArcadeCabinet(program)
    arcade_cabinet.run()
    return ilen(tile for tile in arcade_cabinet.screen.values() if tile == BLOCK_TILE)


if __name__ == "__main__":
    with open("day13.txt") as file_:
        program = file_.read()
    # logging.basicConfig(level=logging.DEBUG)
    print("Part 1:", part1(program))
