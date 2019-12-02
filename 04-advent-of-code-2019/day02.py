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
    initial[1] = 12
    initial[2] = 2
    final = run_intcode_program(initial)
    return final[0]


if __name__ == "__main__":
    with open("day02.txt") as file_:
        values = [int(n) for n in file_.read().split(",")]
    print("Part 1:", part1(values))
