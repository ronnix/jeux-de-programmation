from collections import Counter
from operator import itemgetter

from more_itertools import chunked


def part1(data):
    layers = extract_layers(data, width=25, height=6)
    counts = [Counter(layer) for layer in layers]
    most_zeroes = min(counts, key=itemgetter("0"))
    return most_zeroes["1"] * most_zeroes["2"]


def extract_layers(data, width, height):
    return chunked(data, width * height)


def part2(data):
    layers = extract_layers(data, width=25, height=6)
    image = merge_layers(layers)
    show_image(image, width=25)


def merge_layers(layers):
    for values in zip(*layers):
        for value in values:
            if value == "0":
                yield "\u2B1B"
                break
            if value == "1":
                yield "\u2B1C"
                break


def show_image(pixels, width):
    for line in chunked(pixels, width):
        print("".join(line))


if __name__ == "__main__":
    with open("day08.txt") as file_:
        data = file_.read()
    print("Part 1:", part1(data))
    print("Part 2:")
    part2(data)
