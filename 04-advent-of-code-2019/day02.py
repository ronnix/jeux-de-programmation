from enum import Enum

import pytest


@pytest.mark.parametrize(
    "initial, final",
    [
        (
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
        ),
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ],
)
def test_run_intcode_program(initial, final):
    assert run_intcode_program(initial) == final


class Opcode(Enum):
    ADD = 1
    MUL = 2
    HALT = 99


def run_intcode_program(program, pc=0):
    """
    Tail-recursive version
    """
    opcode = program[pc]
    if opcode == Opcode.HALT.value:
        return program
    elif opcode == Opcode.ADD.value:
        src1, src2, dest, *_ = program[pc + 1 :]
        program[dest] = program[src1] + program[src2]
    elif opcode == Opcode.MUL.value:
        src1, src2, dest, *_ = program[pc + 1 :]
        program[dest] = program[src1] * program[src2]
    else:
        raise ValueError(f"invalid opcode {opcode}")
    return run_intcode_program(program, pc + 4)


def part1(initial):
    memory = initial.copy()
    memory[1] = 12
    memory[2] = 2
    final = run_intcode_program(memory)
    return final[0]


def part2(initial, expected_output):
    for noun in range(0, 100):
        for verb in range(0, 100):
            memory = initial.copy()
            memory[1] = noun
            memory[2] = verb
            final = run_intcode_program(memory)
            if final[0] == expected_output:
                return 100 * noun + verb
    raise RuntimeError("No inputs")


if __name__ == "__main__":
    with open("day02.txt") as file_:
        values = [int(n) for n in file_.read().split(",")]
    print("Part 1:", part1(initial=values))
    print("Part 2:", part2(initial=values, expected_output=19690720))
