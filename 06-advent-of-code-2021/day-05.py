# https://adventofcode.com/2021/day/5

from collections import Counter
from dataclasses import dataclass
from typing import List


SAMPLE_INPUT = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


# === Part 1 ===


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Segment:
    start: Point
    end: Point

    def is_horizontal(self):
        return self.start.y == self.end.y

    def is_vertical(self):
        return self.start.x == self.end.x

    def covered(self):
        lx = self.end.x - self.start.x
        ly = self.end.y - self.start.y
        l = max(abs(lx), abs(ly))
        dx = lx / l
        dy = ly / l
        for i in range(l + 1):
            yield Point(self.start.x + i * dx, self.start.y + i * dy)


def test_parsing():
    segments = parse(SAMPLE_INPUT)
    assert len(segments) == 10
    assert segments[0] == Segment(Point(0, 9), Point(5,9))
    assert segments[0].is_horizontal()
    assert not segments[0].is_vertical()
    assert(len(horizontal_or_vertical_segments(segments))) == 6


def test_part1():
    segments = parse(SAMPLE_INPUT)
    assert part1(segments) == 5


def horizontal_or_vertical_segments(segments: List[Segment]) -> List[Segment]:
    return [s for s in segments if s.is_horizontal() or s.is_vertical()]


def part1(segments: List[Segment]):
    return count_overlapping_points(horizontal_or_vertical_segments(segments))


def count_overlapping_points(segments: List[Segment]):
    counter = Counter()
    for segment in segments:
        for point in segment.covered():
            counter[point] += 1
    points = {point for point, count in counter.items() if count >= 2}
    return len(points)


# === Part 2 ===

def test_part2():
    segments = parse(SAMPLE_INPUT)
    assert part2(segments) == 12


def part2(segments):
    return count_overlapping_points(segments)


# === Input parsing ===


def read_input():
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> List[Segment]:
    return [parse_segment(line) for line in text.splitlines()]


def parse_segment(line: str) -> Segment:
    start, end = line.split(" -> ")
    return Segment(parse_point(start), parse_point(end))


def parse_point(text: str) -> Point:
    x, y = map(int, text.split(","))
    return Point(x, y)


if __name__ == "__main__":
    segments = parse(read_input())
    print("Part 1:", part1(segments))
    print("Part 2:", part2(segments))
