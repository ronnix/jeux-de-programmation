from enum import Enum
from itertools import permutations
from typing import NamedTuple, Tuple

import pytest


class Opcode(Enum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
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
        Opcode.INPUT.value: 1,
        Opcode.OUTPUT.value: 1,
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


class IntcodeComputer:
    def __init__(self, program):
        self.program = [int(n) for n in program.split(",")]

    def run(self, inputs, pc=0):
        outputs = []
        while True:
            instruction = Instruction.decode(self.program[pc])
            if instruction.opcode == Opcode.HALT.value:
                break
            elif instruction.opcode == Opcode.ADD.value:
                src1 = instruction.read_operand(1, self.program, pc)
                src2 = instruction.read_operand(2, self.program, pc)
                instruction.write_operand(3, self.program, pc, src1 + src2)
            elif instruction.opcode == Opcode.MUL.value:
                src1 = instruction.read_operand(1, self.program, pc)
                src2 = instruction.read_operand(2, self.program, pc)
                instruction.write_operand(3, self.program, pc, src1 * src2)
            elif instruction.opcode == Opcode.INPUT.value:
                instruction.write_operand(1, self.program, pc, inputs.pop(0))
            elif instruction.opcode == Opcode.OUTPUT.value:
                outputs.append(instruction.read_operand(1, self.program, pc))
            elif instruction.opcode == Opcode.JUMP_IF_TRUE.value:
                condition = instruction.read_operand(1, self.program, pc)
                target = instruction.read_operand(2, self.program, pc)
                if condition != 0:
                    pc = target
                    continue
            elif instruction.opcode == Opcode.JUMP_IF_FALSE.value:
                condition = instruction.read_operand(1, self.program, pc)
                target = instruction.read_operand(2, self.program, pc)
                if condition == 0:
                    pc = target
                    continue
            elif instruction.opcode == Opcode.LT.value:
                src1 = instruction.read_operand(1, self.program, pc)
                src2 = instruction.read_operand(2, self.program, pc)
                res = 1 if src1 < src2 else 0
                instruction.write_operand(3, self.program, pc, res)
            elif instruction.opcode == Opcode.EQ.value:
                src1 = instruction.read_operand(1, self.program, pc)
                src2 = instruction.read_operand(2, self.program, pc)
                res = 1 if src1 == src2 else 0
                instruction.write_operand(3, self.program, pc, res)
            else:
                raise ValueError(f"invalid opcode {instruction.opcode}")
            pc += instruction.size()
        return outputs


def parse_input(text):
    return [int(n) for n in text.split(",")]


@pytest.mark.parametrize(
    "max_signal,phase_setting,program",
    [
        (43210, (4, 3, 2, 1, 0), "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"),
        (
            54321,
            (0, 1, 2, 3, 4),
            "3,23,3,24,1002,24,10,24,1002,23,-1,23,"
            "101,5,23,23,1,24,23,23,4,23,99,0,0",
        ),
        (
            65210,
            (1, 0, 4, 3, 2),
            "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,"
            "1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
        ),
    ],
)
def test_max_thruster_output_signal(max_signal, phase_setting, program):
    assert max_thruster_output_signal(program) == (max_signal, phase_setting)


def max_thruster_output_signal(program):
    return max(
        (
            thruster_output_signal(program, phase_setting_sequence),
            phase_setting_sequence,
        )
        for phase_setting_sequence in permutations([0, 1, 2, 3, 4])
    )


def thruster_output_signal(program, phase_setting_sequence):
    input_ = 0
    for phase in phase_setting_sequence:
        amp = IntcodeComputer(program)
        outputs = amp.run(inputs=[phase, input_])
        input_ = outputs[0]
    return input_


def part1(program):
    max_signal, _ = max_thruster_output_signal(program)
    return max_signal


if __name__ == "__main__":
    with open("day07.txt") as file_:
        program = file_.read()
    print("Part 1:", part1(program))
