from enum import Enum
from typing import NamedTuple, Tuple

import pytest


class Opcode(Enum):
    ADD = 1
    MUL = 2
    STORE = 3
    LOAD = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LT = 7
    EQ = 8
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
        Opcode.JUMP_IF_TRUE.value: 2,
        Opcode.JUMP_IF_FALSE.value: 2,
        Opcode.LT.value: 3,
        Opcode.EQ.value: 3,
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
        elif instruction.opcode == Opcode.JUMP_IF_TRUE.value:
            condition = instruction.read_operand(1, program, pc)
            target = instruction.read_operand(2, program, pc)
            if condition != 0:
                pc = target
                continue
        elif instruction.opcode == Opcode.JUMP_IF_FALSE.value:
            condition = instruction.read_operand(1, program, pc)
            target = instruction.read_operand(2, program, pc)
            if condition == 0:
                pc = target
                continue
        elif instruction.opcode == Opcode.LT.value:
            src1 = instruction.read_operand(1, program, pc)
            src2 = instruction.read_operand(2, program, pc)
            res = 1 if src1 < src2 else 0
            instruction.write_operand(3, program, pc, res)
        elif instruction.opcode == Opcode.EQ.value:
            src1 = instruction.read_operand(1, program, pc)
            src2 = instruction.read_operand(2, program, pc)
            res = 1 if src1 == src2 else 0
            instruction.write_operand(3, program, pc, res)
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


@pytest.mark.parametrize(
    "program,input_,expected_outputs",
    [
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 7, [0]),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, [1]),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 9, [0]),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7, [1]),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8, [0]),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 9, [0]),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 7, [0]),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, [1]),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 9, [0]),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7, [1]),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8, [0]),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 9, [0]),
    ],
)
def test_comparison(program, input_, expected_outputs):
    program, outputs = run_intcode_program(program, input_=input_)
    assert outputs == expected_outputs


@pytest.mark.parametrize(
    "program,input_,expected_outputs",
    [
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, [0]),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1, [1]),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, [0]),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1, [1]),
    ],
)
def test_jump(program, input_, expected_outputs):
    program, outputs = run_intcode_program(program, input_=input_)
    assert outputs == expected_outputs


@pytest.mark.parametrize(
    "input_,expected_outputs", [(7, [999]), (8, [1000]), (9, [1001]),]
)
def test_larger_example(input_, expected_outputs):
    program = parse_input(
        "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
        "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,"
        "999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
    )
    program, outputs = run_intcode_program(program, input_=input_)
    assert outputs == expected_outputs


def part2(program):
    program, outputs = run_intcode_program(program, 5)
    diagnostic_code = outputs[-1]
    success = all(output == 0 for output in outputs[:-1])
    return success, diagnostic_code


def parse_input(text):
    return [int(n) for n in text.split(",")]


if __name__ == "__main__":
    with open("day05.txt") as file_:
        program = parse_input(file_.read())
    print("Part 1:", part1(program.copy()))
    print("Part 2:", part2(program.copy()))
