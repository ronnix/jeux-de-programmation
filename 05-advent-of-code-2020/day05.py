import pytest


class BoardingPass:
    def __init__(self, chars):
        self.chars = chars

    @property
    def row(self):
        return bsp(self.chars[:7], 0, 127, "F", "B")

    @property
    def column(self):
        return bsp(self.chars[7:], 0, 7, "L", "R")

    @property
    def seat_id(self):
        return self.row * 8 + self.column


def bsp(s, low, high, low_char, high_char):
    if len(s) == 0:
        assert low == high
        assert int(low) == low
        return int(low)
    middle = low + (high - low + 1) / 2
    if s[0] == low_char:
        return bsp(s[1:], low, middle - 1, low_char, high_char)
    elif s[0] == high_char:
        return bsp(s[1:], middle, high, low_char, high_char)
    else:
        raise ValueError


@pytest.mark.parametrize("chars,row,column,seat_id", [
    ("FBFBBFFRLR", 44, 5, 357),
    ("BFFFBBFRRR", 70, 7, 567),
    ("FFFBBBFRRR", 14, 7, 119),
    ("BBFFBBFRLL", 102, 4, 820),
])
def test_boarding_pass_coordinates(chars, row, column, seat_id):
    boarding_pass = BoardingPass(chars)
    assert boarding_pass.row == row
    assert boarding_pass.column == column
    assert boarding_pass.seat_id == seat_id


def part1(boarding_passes):
    return max(boarding_pass.seat_id for boarding_pass in boarding_passes)


def part2(boarding_passes):
    all_seats = set(range(128 * 8))
    taken = {boarding_pass.seat_id for boarding_pass in boarding_passes}
    not_taken = sorted(all_seats - taken)
    result = [seat for seat in not_taken if seat - 1 in taken and seat + 1 in taken]
    assert len(result) == 1
    return result[0]


if __name__ == '__main__':
    with open("day05.txt") as f:
        boarding_passes = [BoardingPass(line.strip()) for line in f]
    print("Part 1:", part1(boarding_passes))
    print("Part 2:", part2(boarding_passes))
