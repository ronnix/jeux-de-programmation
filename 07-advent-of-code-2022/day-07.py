# https://adventofcode.com/2022/day/7

from __future__ import annotations

from typing import Dict

from more_itertools import before_and_after


EXAMPLE_INPUT = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


# === Part 1 ===


def test_part1():
    assert part1(EXAMPLE_INPUT) == 95_437


def part1(text: str) -> int:
    shell = Shell()
    shell.run(text.splitlines())
    return sum(shell.root.sizes_of_subdirs_at_most(100_000))


class Shell:
    def __init__(self):
        self.cwd = self.root = Directory()

    def run(self, lines):
        lines = (Line(line) for line in lines)
        while True:
            line = next(lines, None)
            if line is None:
                break
            _, cmd, *args = line.parts()
            if cmd == "cd":
                self.cd(*args)
            elif cmd == "ls":
                out, lines = before_and_after(Line.is_output, lines)
                self.ls(out)

    def cd(self, path):
        if path == "/":
            self.cwd = self.root
        elif path == "..":
            self.cwd = self.cwd.parent
        else:
            self.cwd = self.cwd.subdirs[path]

    def ls(self, output_lines):
        for line in output_lines:
            size, name = line.parts()
            if size == "dir":
                self.cwd.subdirs[name] = Directory(parent=self.cwd)
            else:
                self.cwd.files[name] = int(size)


class Line:
    def __init__(self, line):
        self.line = line

    def parts(self):
        return self.line.split()

    def is_command(self):
        return self.line.startswith("$")

    def is_output(self):
        return not self.line.startswith("$")


class Directory:
    files: Dict[str, int]
    subdirs: Dict[str, Directory]

    def __init__(self, parent=None):
        self.parent = parent
        self.files = {}
        self.subdirs = {}

    def size(self):
        return sum(self.files.values()) + sum(
            subdir.size() for subdir in self.subdirs.values()
        )

    def sizes_of_subdirs_at_most(self, n):
        if (size := self.size()) <= n:
            yield size
        for subdir in self.subdirs.values():
            yield from subdir.sizes_of_subdirs_at_most(n)

    def sizes_of_subdirs_at_least(self, n):
        if (size := self.size()) >= n:
            yield size
        for subdir in self.subdirs.values():
            yield from subdir.sizes_of_subdirs_at_least(n)


# === Part 2 ===


def test_part2():
    assert part2(EXAMPLE_INPUT) == 24_933_642


def part2(text: str) -> int:
    shell = Shell()
    shell.run(text.splitlines())

    total_space = 70_000_000
    used_space = shell.root.size()
    available_space = total_space - used_space
    need_to_free = 30_000_000 - available_space

    return sorted(shell.root.sizes_of_subdirs_at_least(need_to_free))[0]


def read_puzzle_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


if __name__ == "__main__":
    text = read_puzzle_input()
    print("Part 1:", part1(text))
    print("Part 2:", part2(text))
