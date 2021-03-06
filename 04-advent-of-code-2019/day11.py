import logging
from array import array
from enum import Enum
from typing import NamedTuple, Tuple

logger = logging.getLogger(__name__)


class Opcode(Enum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LT = 7
    EQ = 8
    OFFSET_REL_BASE = 9
    HALT = 99


class AddressingMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Instruction(NamedTuple):
    opcode: Opcode
    modes: Tuple[AddressingMode, AddressingMode, AddressingMode]

    @classmethod
    def decode(cls, value):
        mode3 = value // 10000
        mode2 = (value // 1000) % 10
        mode1 = (value // 100) % 10
        opcode = value % 100
        return cls(opcode, (mode1, mode2, mode3))

    _operands = {
        Opcode.ADD.value: 3,
        Opcode.MUL.value: 3,
        Opcode.INPUT.value: 1,
        Opcode.OUTPUT.value: 1,
        Opcode.JUMP_IF_TRUE.value: 2,
        Opcode.JUMP_IF_FALSE.value: 2,
        Opcode.LT.value: 3,
        Opcode.EQ.value: 3,
        Opcode.OFFSET_REL_BASE.value: 1,
    }

    def nb_operands(self):
        return self._operands[self.opcode]

    def size(self):
        return 1 + self.nb_operands()

    def operand_mode(self, n):
        return self.modes[n - 1]


SIGNED_LONG = "l"


class IntcodeComputer:
    def __init__(self, program, memory_size=1024 * 1024):
        self.memory = array(SIGNED_LONG, [int(n) for n in program.split(",")])
        self.memory.extend([0] * (memory_size - len(self.memory)))
        self.pc = 0
        self.relative_base = 0

    def run(self):
        while True:
            logger.debug("PC = %s", self.pc)
            instruction = Instruction.decode(self.memory[self.pc])

            if instruction.opcode == Opcode.HALT.value:
                logger.debug("HALT")
                break

            elif instruction.opcode == Opcode.ADD.value:
                src1 = self.read_operand(instruction, 1)
                src2 = self.read_operand(instruction, 2)
                dst = self.get_effective_address(instruction, 3)
                logger.debug("ADD %s, %s -> %s", src1, src2, dst)
                self.memory[dst] = src1 + src2

            elif instruction.opcode == Opcode.MUL.value:
                src1 = self.read_operand(instruction, 1)
                src2 = self.read_operand(instruction, 2)
                dst = self.get_effective_address(instruction, 3)
                logger.debug("MUL %s, %s -> %s", src1, src2, dst)
                self.memory[dst] = src1 * src2

            elif instruction.opcode == Opcode.INPUT.value:
                dst = self.get_effective_address(instruction, 1)
                logger.debug("INPUT -> %s", dst)
                value = yield
                logger.debug(f"(received {value})")
                assert value is not None
                self.memory[dst] = value

            elif instruction.opcode == Opcode.OUTPUT.value:
                value = self.read_operand(instruction, 1)
                logger.debug("OUTPUT %s", value)
                yield value

            elif instruction.opcode == Opcode.JUMP_IF_TRUE.value:
                condition = self.read_operand(instruction, 1)
                target = self.read_operand(instruction, 2)
                logger.debug("JUMP_IF_TRUE %s -> %s", condition, target)
                if condition != 0:
                    self.pc = target
                    continue

            elif instruction.opcode == Opcode.JUMP_IF_FALSE.value:
                condition = self.read_operand(instruction, 1)
                target = self.read_operand(instruction, 2)
                logger.debug("JUMP_IF_FALSE %s -> %s", condition, target)
                if condition == 0:
                    self.pc = target
                    continue

            elif instruction.opcode == Opcode.LT.value:
                src1 = self.read_operand(instruction, 1)
                src2 = self.read_operand(instruction, 2)
                dst = self.get_effective_address(instruction, 3)
                logger.debug("LT %s, %s -> %s", src1, src2, dst)
                self.memory[dst] = 1 if src1 < src2 else 0

            elif instruction.opcode == Opcode.EQ.value:
                src1 = self.read_operand(instruction, 1)
                src2 = self.read_operand(instruction, 2)
                dst = self.get_effective_address(instruction, 3)
                logger.debug("EQ %s, %s -> %s", src1, src2, dst)
                self.memory[dst] = 1 if src1 == src2 else 0

            elif instruction.opcode == Opcode.OFFSET_REL_BASE.value:
                offset = self.read_operand(instruction, 1)
                logger.debug("OFFSET_REL_BASE %s", offset)
                self.relative_base += offset

            else:
                raise ValueError(f"invalid opcode {instruction.opcode}")

            self.pc += instruction.size()

    def read_operand(self, instruction, n):
        assert n <= instruction.nb_operands()
        value = self.memory[self.pc + n]
        mode = instruction.operand_mode(n)
        if mode == AddressingMode.IMMEDIATE.value:
            return value
        elif mode == AddressingMode.POSITION.value:
            return self.memory[value]
        elif mode == AddressingMode.RELATIVE.value:
            return self.memory[self.relative_base + value]
        else:
            raise ValueError(f"Invalid addressing mode {mode}")

    def get_effective_address(self, instruction, n):
        assert n <= instruction.nb_operands()
        mode = instruction.operand_mode(n)
        if mode == AddressingMode.POSITION.value:
            return self.memory[self.pc + n]
        elif mode == AddressingMode.RELATIVE.value:
            displacement = self.memory[self.pc + n]
            return self.relative_base + displacement
        else:
            raise ValueError(f"Invalid addressing mode {mode}")


UP = (0, 1)
LEFT = (-1, 0)
DOWN = (0, -1)
RIGHT = (1, 0)


TURN_LEFT = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}
TURN_RIGHT = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}


class HullPaintingRobot:
    def __init__(self, program):
        self.computer = IntcodeComputer(program)
        self.position = (0, 0)
        self.direction = UP
        self.grid = {}

    def run(self):
        coroutine = self.computer.run()
        try:
            while True:
                next(coroutine)

                logger.debug("Robot is at %s facing %s", self.position, self.direction)

                panel_color = self.grid.get(self.position, 0)
                logger.debug("Panel color is %s", panel_color)

                color_to_paint = coroutine.send(panel_color)
                self.paint_current_panel(color_to_paint)

                new_direction = next(coroutine)
                if new_direction == 0:
                    self.turn_left()
                elif new_direction == 1:
                    self.turn_right()
                else:
                    raise ValueError(f"Invalid direction {new_direction}")

                self.move_forward()
        except StopIteration:
            logger.debug("Program terminated")

    def paint_current_panel(self, color):
        if color not in {0, 1}:
            raise ValueError(f"Invalid color {color}")
        logger.debug("Painting panel %s with %s", self.position, color)
        self.grid[self.position] = color

    def turn_left(self):
        logger.debug("Turning left")
        self.direction = TURN_LEFT[self.direction]

    def turn_right(self):
        logger.debug("Turning right")
        self.direction = TURN_RIGHT[self.direction]

    def move_forward(self):
        logger.debug("Moving forward")
        self.position = (
            self.position[0] + self.direction[0],
            self.position[1] + self.direction[1],
        )

    def number_of_painted_panels(self):
        return len(self.grid)

    def print_grid(self):
        min_x = min(p[0] for p in self.grid)
        max_x = max(p[0] for p in self.grid)
        min_y = min(p[1] for p in self.grid)
        max_y = max(p[1] for p in self.grid)
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                color = self.grid.get((x, y), 0)
                print("\u2B1B" if color == 0 else "\u2B1C", end="")
            print()


def parse_input(text):
    return [int(n) for n in text.split(",")]


def part1(program):
    robot = HullPaintingRobot(program)
    robot.run()
    return robot.number_of_painted_panels()


def part2(program):
    robot = HullPaintingRobot(program)
    robot.grid[(0, 0)] = 1  # start on a white panel
    robot.run()
    robot.print_grid()


if __name__ == "__main__":
    with open("day11.txt") as file_:
        program = file_.read()
    # logging.basicConfig(level=logging.DEBUG)
    print("Part 1:", part1(program))
    print("Part 2:")
    part2(program)
