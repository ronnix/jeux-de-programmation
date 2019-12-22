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
    def __init__(self, program, input_callback, memory_size=1024 * 1024):
        self.memory = array(SIGNED_LONG, [int(n) for n in program.split(",")])
        self.memory.extend([0] * (memory_size - len(self.memory)))
        self.pc = 0
        self.relative_base = 0
        self.input_callback = input_callback

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
                value = self.input_callback()
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
