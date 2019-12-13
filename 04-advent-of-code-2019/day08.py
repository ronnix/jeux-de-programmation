from collections import Counter
from operator import itemgetter

from more_itertools import chunked


def part1(data):
    layers = decode_space_image_format(data, width=25, height=6)
    counts = [Counter(layer) for layer in layers]
    most_zeroes = min(counts, key=itemgetter("0"))
    return most_zeroes["1"] * most_zeroes["2"]


def decode_space_image_format(data, width, height):
    return chunked(data, width * height)


if __name__ == "__main__":
    with open("day08.txt") as file_:
        data = file_.read()
    print("Part 1:", part1(data))
