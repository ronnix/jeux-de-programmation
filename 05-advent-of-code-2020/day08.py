from textwrap import dedent

import pytest


@pytest.fixture
def sample_program():
    return load_program(
        dedent(
            """
            nop +0
            acc +1
            jmp +4
            acc +3
            jmp -3
            acc -99
            acc +1
            jmp -4
            acc +6
            """
        )
    )


def test_run(sample_program):
    with pytest.raises(InfiniteLoop) as exc:
        run(sample_program)
    assert exc.value.accumulator == 5


def load_program(text):
    return [parse_instruction(line.strip()) for line in text.splitlines() if line]


def parse_instruction(line):
    instruction, operand = line.split(" ")
    return instruction, int(operand)


def run(program):
    program_counter = 0
    accumulator = 0
    already_executed = set()
    while True:
        if program_counter in already_executed:
            raise InfiniteLoop(accumulator)
        already_executed.add(program_counter)
        if program_counter == len(program):
            return accumulator
        instruction, operand = program[program_counter]
        if instruction == "nop":
            program_counter += 1
        elif instruction == "acc":
            accumulator += operand
            program_counter += 1
        elif instruction == "jmp":
            program_counter += operand


class InfiniteLoop(Exception):
    def __init__(self, accumulator):
        self.accumulator = accumulator


def part1(program):
    try:
        run(program)
    except InfiniteLoop as exc:
        return exc.accumulator


def test_fix_program(sample_program):
    assert fix_program(sample_program) == 8


def fix_program(program):
    for index, (instruction, operand) in enumerate(program):
        try:
            if instruction == "nop":
                return run(program[:index] + [("jmp", operand)] + program[index + 1 :])
            elif instruction == "jmp":
                return run(program[:index] + [("nop", operand)] + program[index + 1 :])
        except InfiniteLoop:
            pass


def part2(program):
    return fix_program(program)


if __name__ == "__main__":
    with open("day08.txt") as f:
        program = load_program(f.read())
    print("Part 1:", part1(program))
    print("Part 2:", part2(program))
