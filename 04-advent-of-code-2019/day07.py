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

    def run(self, pc=0):
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
                value = yield
                instruction.write_operand(1, self.program, pc, value)
            elif instruction.opcode == Opcode.OUTPUT.value:
                value = instruction.read_operand(1, self.program, pc)
                yield value
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
    for phase_setting in phase_setting_sequence:
        amp = IntcodeComputer(program)
        coroutine = amp.run()
        next(coroutine)  # start coroutine
        coroutine.send(phase_setting)
        input_ = coroutine.send(input_)
    return input_


def part1(program):
    max_signal, _ = max_thruster_output_signal(program)
    return max_signal


@pytest.mark.parametrize(
    "max_signal,phase_setting,program",
    [
        (
            139629729,
            (9, 8, 7, 6, 5),
            "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,"
            "27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
        ),
        (
            18216,
            (9, 7, 8, 5, 6),
            "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,"
            "-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,"
            "53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10",
        ),
    ],
)
def test_max_thruster_output_signal_feedback_mode(max_signal, phase_setting, program):
    assert max_thruster_output_signal_feedback_mode(program) == (
        max_signal,
        phase_setting,
    )


def max_thruster_output_signal_feedback_mode(program):
    return max(
        (
            thruster_output_signal_feedback_mode(program, phase_setting_sequence),
            phase_setting_sequence,
        )
        for phase_setting_sequence in permutations([5, 6, 7, 8, 9])
    )


def thruster_output_signal_feedback_mode(program, phase_setting_sequence):
    # Initialize amps
    amps = {}
    for i, phase_setting in enumerate(phase_setting_sequence):
        amps[chr(ord("A") + i)] = coroutine = IntcodeComputer(program).run()
        next(coroutine)  # start execution
        coroutine.send(phase_setting)

    # Feedback loop
    input_ = 0
    running = set(amps)
    while running:
        for name, coroutine in amps.items():
            if name not in running:
                continue
            input_ = coroutine.send(input_)  # get output to feed as next input
            try:
                next(coroutine)  # continue running
            except StopIteration:
                running.remove(name)  # halt
    return input_


def part2(program):
    max_signal, _ = max_thruster_output_signal_feedback_mode(program)
    return max_signal


if __name__ == "__main__":
    with open("day07.txt") as file_:
        program = file_.read()
    print("Part 1:", part1(program))
    print("Part 2:", part2(program))
