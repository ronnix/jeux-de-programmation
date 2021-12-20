# https://adventofcode.com/2021/day/16

from contextlib import contextmanager
from dataclasses import dataclass
from time import monotonic
from typing import Iterator, List

from bitstring import BitStream
import pytest


# === Part 1 ===


@dataclass
class Packet:
    version: int

    def sum_versions(self) -> int:
        return self.version


@dataclass
class Value(Packet):
    value: int


@dataclass
class Operator(Packet):
    type_: int
    sub_packets: List[Packet]

    def sum_versions(self) -> int:
        return self.version + sum(s.sum_versions() for s in self.sub_packets)


def test_parse_value():
    stream = parse("D2FE28")
    assert stream.bin == "110100101111111000101000"

    value = parse_packet(stream)
    assert value.version == 6
    assert value.value == 2021


def test_parse_operator():
    stream = parse("38006F45291200")
    assert stream.bin == "00111000000000000110111101000101001010010001001000000000"

    operator = parse_packet(stream)
    assert operator.version == 1
    assert operator.type_ == 6
    assert len(operator.sub_packets) == 2


def test_parse_operator_2():
    stream = parse("EE00D40C823060")
    assert stream.bin == "11101110000000001101010000001100100000100011000001100000"

    operator = parse_packet(stream)
    assert operator.version == 7
    assert operator.type_ == 3
    assert len(operator.sub_packets) == 3


@pytest.mark.parametrize(
    "packet,result",
    [
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31),
    ],
)
def test_sum_versions(packet, result):
    stream = parse(packet)
    assert parse_packet(stream).sum_versions() == result


def parse_packet(stream: BitStream) -> Packet:
    version = stream.read(3).uint
    type_ = stream.read(3).uint
    if type_ == 4:
        return parse_value(version, stream)
    else:
        return parse_operator(version, type_, stream)


def parse_value(version: int, stream: BitStream) -> Value:
    value = BitStream()
    while True:
        group = stream.read(5)
        last_group = not group.read(1)
        value += group.read(4)
        if last_group:
            return Value(version=version, value=value.uint)


def parse_operator(version: int, type_: int, stream: BitStream) -> Operator:
    length_type_id = stream.read(1)
    sub_packets = []
    if length_type_id:
        nb_sub_packets = stream.read(11).uint
        for _ in range(nb_sub_packets):
            sub_packets.append(parse_packet(stream))
    else:
        bit_length = stream.read(15).uint
        sub_packet_data = stream.read(bit_length)
        while sub_packet_data.pos < bit_length:
            sub_packets.append(parse_packet(sub_packet_data))
    return Operator(version=version, type_=type_, sub_packets=sub_packets)


def part1(stream: str) -> int:
    return parse_packet(stream).sum_versions()


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> BitStream:
    return BitStream("0x" + text)


@contextmanager
def timer() -> Iterator:
    start = monotonic()
    yield
    duration = monotonic() - start
    print(f"{duration:0.1f}s")


if __name__ == "__main__":
    stream = parse(read_input())
    with timer():
        print("Part 1:", part1(stream))
