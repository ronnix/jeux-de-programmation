# https://adventofcode.com/2021/day/18

from dataclasses import dataclass
from enum import Enum
from itertools import permutations, pairwise  # Python ≥ 3.10
from typing import Any, Iterator, List, Optional, Union, Tuple

from more_itertools import peekable
import pytest


SAMPLE_INPUT = """\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""


# === Part 1 ===


class Direction(Enum):
    Left = 0
    Right = 1


Path = List[Direction]


@dataclass
class SnailFishNumber:
    children: Tuple[Union[int, "SnailFishNumber"], Union[int, "SnailFishNumber"]]

    def __init__(
        self, left: Union[int, "SnailFishNumber"], right: Union[int, "SnailFishNumber"]
    ):
        self.children = (left, right)

    def __repr__(self) -> str:
        return f"[{self.left!r},{self.right!r}]"

    @property
    def left(self) -> Union[int, "SnailFishNumber"]:
        return self.children[Direction.Left.value]

    @property
    def right(self) -> Union[int, "SnailFishNumber"]:
        return self.children[Direction.Right.value]

    @classmethod
    def from_string(cls, text: str) -> "SnailFishNumber":
        return cls.from_list(eval(text))

    @classmethod
    def from_list(cls, list_: List[Any]) -> "SnailFishNumber":
        left, right = list_
        return cls(
            left=left if isinstance(left, int) else cls.from_list(left),
            right=right if isinstance(right, int) else cls.from_list(right),
        )

    def __add__(self, other: "SnailFishNumber") -> "SnailFishNumber":
        return SnailFishNumber(self, other).reduce()

    def dfs(self) -> Iterator[Tuple[int, Path]]:
        return self._dfs(path=[])

    def _dfs(self, path: Path) -> Iterator[Tuple[int, Path]]:
        for direction in (Direction.Left, Direction.Right):
            child = self.children[direction.value]
            if isinstance(child, int):
                yield (child, path + [direction])
            else:
                yield from child._dfs(path=path + [direction])

    def reduce(self) -> "SnailFishNumber":
        number = self
        while True:
            exploded = number.explode()
            if isinstance(exploded, SnailFishNumber):
                number = exploded
                continue
            splitted = number.split()
            if isinstance(splitted, SnailFishNumber):
                number = splitted
                continue
            return number

    def explode(self) -> Optional[Union[int, "SnailFishNumber"]]:
        prev_path = None
        nodes = peekable(self.dfs())
        for first, second in pairwise(nodes):
            value1, path1 = first
            value2, path2 = second
            if len(path1) == len(path2) == 5 and path1[:4] == path2[:4]:
                nodes_to_update = []
                if prev_path:
                    nodes_to_update.append((prev_path, value1))
                _, next_path = nodes.peek((None, None))
                if next_path:
                    nodes_to_update.append((next_path, value2))
                return self._explode(
                    path=[], path_to_explode=path1[:4], nodes_to_update=nodes_to_update
                )
            prev_path = path1
        return None

    def _explode(
        self, path: Path, path_to_explode: Path, nodes_to_update: List[Tuple[Path, int]]
    ) -> Union[int, "SnailFishNumber"]:
        if path == path_to_explode:
            return 0

        left: Union[int, SnailFishNumber]
        if isinstance(self.left, int):
            left = self.left
            for u_path, u_value in nodes_to_update:
                if u_path == path + [Direction.Left]:
                    left += u_value
        else:
            left = self.left._explode(
                path=path + [Direction.Left],
                path_to_explode=path_to_explode,
                nodes_to_update=nodes_to_update,
            )

        right: Union[int, SnailFishNumber]
        if isinstance(self.right, int):
            right = self.right
            for u_path, u_value in nodes_to_update:
                if u_path == path + [Direction.Right]:
                    right += u_value
        else:
            right = self.right._explode(
                path=path + [Direction.Right],
                path_to_explode=path_to_explode,
                nodes_to_update=nodes_to_update,
            )

        return SnailFishNumber(left, right)

    def split(self) -> Optional["SnailFishNumber"]:
        for value, path in self.dfs():
            if value >= 10:
                return self._split(path=[], path_to_split=path)
        return None

    def _split(self, path: Path, path_to_split: Path) -> "SnailFishNumber":
        left: Union[int, SnailFishNumber]
        if isinstance(self.left, int):
            if path + [Direction.Left] == path_to_split:
                left = self._split_number(self.left)
            else:
                left = self.left
        else:
            left = self.left._split(
                path=path + [Direction.Left],
                path_to_split=path_to_split,
            )

        right: Union[int, SnailFishNumber]
        if isinstance(self.right, int):
            if path + [Direction.Right] == path_to_split:
                right = self._split_number(self.right)
            else:
                right = self.right
        else:
            right = self.right._split(
                path=path + [Direction.Right],
                path_to_split=path_to_split,
            )

        return SnailFishNumber(left, right)

    @staticmethod
    def _split_number(n: int) -> "SnailFishNumber":
        s_l = n // 2
        s_r = n - s_l
        return SnailFishNumber(left=s_l, right=s_r)

    def magnitude(self) -> int:
        return 3 * (
            self.left if isinstance(self.left, int) else self.left.magnitude()
        ) + 2 * (self.right if isinstance(self.right, int) else self.right.magnitude())


S = SnailFishNumber


def test_parse() -> None:
    assert S.from_string("[1,2]") == S(1, 2)


def test_add() -> None:
    res = S.from_string("[1,2]") + S.from_string("[[3,4],5]")
    assert res == S.from_string("[[1,2],[[3,4],5]]")


def test_dfs() -> None:
    n = S.from_string("[[[[[9,8],1],2],3],4]")
    assert list(n.dfs()) == [
        (
            9,
            [
                Direction.Left,
                Direction.Left,
                Direction.Left,
                Direction.Left,
                Direction.Left,
            ],
        ),
        (
            8,
            [
                Direction.Left,
                Direction.Left,
                Direction.Left,
                Direction.Left,
                Direction.Right,
            ],
        ),
        (1, [Direction.Left, Direction.Left, Direction.Left, Direction.Right]),
        (2, [Direction.Left, Direction.Left, Direction.Right]),
        (3, [Direction.Left, Direction.Right]),
        (4, [Direction.Right]),
    ]


def test_explode() -> None:
    n = S.from_string("[[[[[9,8],1],2],3],4]")
    assert n.explode() == S.from_string("[[[[0,9],2],3],4]")


def test_add_and_reduce() -> None:
    res = S.from_string("[[[[4,3],4],4],[7,[[8,4],9]]]") + S.from_string("[1,1]")
    assert res == S.from_string("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")


def test_sum_1() -> None:
    numbers = parse("[1,1]\n[2,2]\n[3,3]\n[4,4]")
    assert snail_sum(numbers) == S.from_string("[[[[1,1],[2,2]],[3,3]],[4,4]]")


def test_sum_2() -> None:
    numbers = parse("[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]")
    assert snail_sum(numbers) == S.from_string("[[[[3,0],[5,3]],[4,4]],[5,5]]")


def test_sum_3() -> None:
    numbers = parse("[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]\n[6,6]")
    assert snail_sum(numbers) == S.from_string("[[[[5,0],[7,4]],[5,5]],[6,6]]")


def test_larger_sum() -> None:
    numbers = parse(
        """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""
    )
    assert snail_sum(numbers) == S.from_string(
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
    )


def snail_sum(numbers: List[SnailFishNumber]) -> SnailFishNumber:
    result = numbers[0]
    for number in numbers[1:]:
        print
        result += number
    return result


@pytest.mark.parametrize(
    "number,magnitude",
    [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ],
)
def test_magnitude(number: str, magnitude: int) -> None:
    assert S.from_string(number).magnitude() == magnitude


def test_magnitude_of_sum() -> None:
    numbers = parse(SAMPLE_INPUT)
    assert snail_sum(numbers).magnitude() == 4140


def part1(numbers: List[SnailFishNumber]) -> int:
    return snail_sum(numbers).magnitude()


# === Part 2 ===


def test_largest_magnitude_of_any_sum_of_two() -> None:
    numbers = parse(SAMPLE_INPUT)
    assert largest_magnitude_of_any_sum_of_two(numbers) == 3993


def largest_magnitude_of_any_sum_of_two(numbers: List[SnailFishNumber]) -> int:
    return max((a + b).magnitude() for a, b in permutations(numbers, 2))


def part2(numbers: List[SnailFishNumber]) -> int:
    return largest_magnitude_of_any_sum_of_two(numbers)


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> List[SnailFishNumber]:
    return [SnailFishNumber.from_string(line) for line in text.splitlines()]


if __name__ == "__main__":
    target = parse(read_input())
    print("Part 1:", part1(target))
    print("Part 2:", part2(target))
