from enum import Enum
from typing import NamedTuple, Tuple

import pytest


class Opcode(Enum):
    ADD = 1
    MUL = 2
    STORE = 3
    LOAD = 4
    HALT = 99


class AddressingMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


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
        Opcode.STORE.value: 1,
        Opcode.LOAD.value: 1,
    }

    def nb_operands(self):
        return self._operands[self.opcode]

    def size(self):
        return 1 + self.nb_operands()

    def operand_mode(self, n):
        return self.modes[n - 1]

    def read_operand(self, n, memory, pc):
        assert n <= self.nb_operands()
        mode = self.operand_mode(n)
        value = memory[pc + n]
        if mode == AddressingMode.IMMEDIATE.value:
            return value
        elif mode == AddressingMode.POSITION.value:
            return memory[value]
        else:
            raise ValueError(f"Invalid addressing mode {mode}")

    def write_operand(self, n, memory, pc, value):
        assert n <= self.nb_operands()
        address = memory[pc + n]
        memory[address] = value


def run_intcode_program(program, input_, pc=0):
    outputs = []
    while True:
        instruction = Instruction.decode(program[pc])
        if instruction.opcode == Opcode.HALT.value:
            break
        elif instruction.opcode == Opcode.ADD.value:
            src1 = instruction.read_operand(1, program, pc)
            src2 = instruction.read_operand(2, program, pc)
            instruction.write_operand(3, program, pc, src1 + src2)
        elif instruction.opcode == Opcode.MUL.value:
            src1 = instruction.read_operand(1, program, pc)
            src2 = instruction.read_operand(2, program, pc)
            instruction.write_operand(3, program, pc, src1 * src2)
        elif instruction.opcode == Opcode.STORE.value:
            instruction.write_operand(1, program, pc, input_)
        elif instruction.opcode == Opcode.LOAD.value:
            outputs.append(instruction.read_operand(1, program, pc))
        else:
            raise ValueError(f"invalid opcode {instruction.opcode}")
        pc += instruction.size()
    return program, outputs


@pytest.mark.parametrize("instruction, opcode, modes", [(1002, 2, (0, 1, 0)),])
def test_decode(instruction, opcode, modes):
    assert Instruction.decode(instruction) == (opcode, modes)


def part1(program):
    program, outputs = run_intcode_program(program, 1)
    diagnostic_code = outputs[-1]
    success = all(output == 0 for output in outputs[:-1])
    return success, diagnostic_code


if __name__ == "__main__":
    with open("day05.txt") as file_:
        program = [int(n) for n in file_.read().split(",")]
    print("Part 1:", part1(program))
