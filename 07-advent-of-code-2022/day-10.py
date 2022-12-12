# https://adventofcode.com/2022/day/10

from typing import Generator, List


EXAMPLE_INPUT = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""


# === Part 1 ===


def test_part1():
    assert part1(EXAMPLE_INPUT) == 13140


def part1(text: str) -> int:
    cpu = CPU(program=text.splitlines())
    sum_of_signal_strengths = 0
    for elapsed_cycles, x in cpu.run():
        if (elapsed_cycles - 20) % 40 == 0:
            sum_of_signal_strengths += elapsed_cycles * x
    return sum_of_signal_strengths


Instruction = str


class CPU:
    def __init__(self, program: List[Instruction]):
        self.program = program
        self.elapsed_cycles = 0
        self.x = 1

    def run(self) -> Generator:
        for instruction in self.program:
            yield from self.run_inst(instruction)
        yield self.elapsed_cycles, self.x

    def run_inst(self, instruction: Instruction) -> Generator:
        opcode, *args = instruction.split()
        match opcode:
            case "addx":
                self.elapsed_cycles += 1
                yield self.elapsed_cycles, self.x
                self.elapsed_cycles += 1
                yield self.elapsed_cycles, self.x
                self.x += int(args[0])
            case "noop":
                self.elapsed_cycles += 1
                yield self.elapsed_cycles, self.x


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
