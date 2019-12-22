import logging

from more_itertools import ilen

from intcode import IntcodeComputer


logger = logging.getLogger(__name__)


EMPTY_TILE = 0
WALL_TILE = 1
BLOCK_TILE = 2
PADDLE_TILE = 3
BALL_TILE = 4

TILE = {
    EMPTY_TILE: "⬛",
    WALL_TILE: "⬜",
    BLOCK_TILE: "⬜",
    PADDLE_TILE: "🔼",
    BALL_TILE: "⚽",
}


class ArcadeCabinet:
    def __init__(self, program, free_play=False, display=False):
        self.computer = IntcodeComputer(program, input_callback=self.autoplay)
        if free_play:
            self.computer.memory[0] = 2
        self.screen = {}
        self.score = 0
        self.display = display

    def run(self):
        coroutine = self.computer.run()
        try:
            while True:
                x, y, tile = next(coroutine), next(coroutine), next(coroutine)
                logger.debug((x, y, tile))
                if (x, y) == (-1, 0):
                    self.score = tile
                else:
                    self.screen[(y, x)] = tile
                if self.display:
                    self.repaint_screen()
        except StopIteration:
            logger.debug("Program terminated")

    def ball_position(self):
        return next(pos for pos, tile in self.screen.items() if tile == BALL_TILE)

    def paddle_position(self):
        return next(pos for pos, tile in self.screen.items() if tile == PADDLE_TILE)

    def autoplay(self):
        _, ball_x = self.ball_position()
        _, paddle_x = self.paddle_position()
        if ball_x < paddle_x:
            return -1
        if ball_x == paddle_x:
            return 0
        if ball_x > paddle_x:
            return 1

    def clear_screen(self):
        print("\033[2J\033[;H")

    def repaint_screen(self):
        self.clear_screen()
        print("Score:", self.score)
        for y in range(23):
            for x in range(43):
                print(TILE[self.screen.get((y, x), 0)], end="")
            print()


def part1(program):
    arcade_cabinet = ArcadeCabinet(program)
    arcade_cabinet.run()
    return ilen(tile for tile in arcade_cabinet.screen.values() if tile == BLOCK_TILE)


def part2(program):
    arcade_cabinet = ArcadeCabinet(program, free_play=True)
    arcade_cabinet.run()
    return arcade_cabinet.score


if __name__ == "__main__":
    with open("day13.txt") as file_:
        program = file_.read()
    # logging.basicConfig(level=logging.DEBUG)
    print("Part 1:", part1(program))
    print("Part 2:", part2(program))
