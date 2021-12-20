# https://adventofcode.com/2021/day/16

from dataclasses import dataclass
from functools import reduce
from typing import Iterable, Iterator, List
import operator

from bitstring import BitStream
import pytest


# === Part 1 ===


@dataclass
class Packet:
    version: int

    @staticmethod
    def parse(stream: BitStream) -> "Packet":
        version = stream.read(3).uint
        type_ = stream.read(3).uint
        if type_ == 4:
            return Value.parse(version, stream)
        else:
            return Operator.parse(version, type_, stream)

    def sum_versions(self) -> int:
        raise NotImplementedError

    def evaluate(self) -> int:
        raise NotImplementedError


@dataclass
class Value(Packet):
    value: int

    @staticmethod
    def parse(version: int, stream: BitStream) -> "Value":
        value = BitStream()
        while True:
            group = stream.read(5)
            last_group = not group.read(1)
            value += group.read(4)
            if last_group:
                return Value(version=version, value=value.uint)

    def sum_versions(self) -> int:
        return self.version

    def evaluate(self) -> int:
        return self.value


@dataclass
class Operator(Packet):
    type_: int
    sub_packets: List[Packet]

    @staticmethod
    def parse(version: int, type_: int, stream: BitStream) -> "Operator":
        length_type_id = stream.read(1)
        sub_packets = []
        if length_type_id:
            nb_sub_packets = stream.read(11).uint
            for _ in range(nb_sub_packets):
                sub_packets.append(Packet.parse(stream))
        else:
            bit_length = stream.read(15).uint
            sub_packet_data = stream.read(bit_length)
            while sub_packet_data.pos < bit_length:
                sub_packets.append(Packet.parse(sub_packet_data))
        return Operator(version=version, type_=type_, sub_packets=sub_packets)

    def sum_versions(self) -> int:
        return self.version + sum(s.sum_versions() for s in self.sub_packets)

    def evaluate(self) -> int:
        match self.type_:
            case 0:
                return sum(s.evaluate() for s in self.sub_packets)
            case 1:
                return product(s.evaluate() for s in self.sub_packets)
            case 2:
                return min(s.evaluate() for s in self.sub_packets)
            case 3:
                return max(s.evaluate() for s in self.sub_packets)
            case 5:
                first = self.sub_packets[0].evaluate()
                second = self.sub_packets[1].evaluate()
                return int(first > second)
            case 6:
                first = self.sub_packets[0].evaluate()
                second = self.sub_packets[1].evaluate()
                return int(first < second)
            case 7:
                first = self.sub_packets[0].evaluate()
                second = self.sub_packets[1].evaluate()
                return int(first == second)
            case _:
                raise NotImplementedError


def product(values: Iterable[int]) -> int:
    return reduce(operator.mul, values, 1)


def test_parse_value():
    stream = parse("D2FE28")
    assert stream.bin == "110100101111111000101000"

    value = Packet.parse(stream)
    assert value.version == 6
    assert value.value == 2021


def test_parse_operator():
    stream = parse("38006F45291200")
    assert stream.bin == "00111000000000000110111101000101001010010001001000000000"

    operator = Packet.parse(stream)
    assert operator.version == 1
    assert operator.type_ == 6
    assert len(operator.sub_packets) == 2


def test_parse_operator_2():
    stream = parse("EE00D40C823060")
    assert stream.bin == "11101110000000001101010000001100100000100011000001100000"

    operator = Packet.parse(stream)
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
    assert Packet.parse(stream).sum_versions() == result


def part1(stream: str) -> int:
    return Packet.parse(stream).sum_versions()


# === Part 2 ===


@pytest.mark.parametrize(
    "packet,result",
    [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ],
)
def test_evaluate(packet, result):
    stream = parse(packet)
    assert Packet.parse(stream).evaluate() == result


def part2(stream: str) -> int:
    return Packet.parse(stream).evaluate()


# === Input parsing ===


def read_input() -> str:
    with open(__file__.removesuffix("py") + "txt") as f:
        return f.read()


def parse(text: str) -> BitStream:
    return BitStream("0x" + text)


if __name__ == "__main__":
    print("Part 1:", part1(parse(read_input())))
    print("Part 2:", part2(parse(read_input())))
