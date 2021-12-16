import os
from functools import reduce
from dataclasses import dataclass


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return open(input_path).read()


def get_mapping(mapping_file):
    mapping_file = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", mapping_file
    )
    mapping = dict()
    for line in open(mapping_file).readlines():
        hexa, binary = line.strip().split(" = ")
        mapping[hexa] = binary
    return mapping


def hex2bin(message, mapping):
    bin = ""
    for hex_symbol in message:
        bin += mapping[hex_symbol]
    return bin


@dataclass
class Packet:
    type: int
    version: int
    length: int


@dataclass
class Operator(Packet):
    size_type: int
    size_param: int


@dataclass
class Literal(Packet):
    value: int
    type: int


def get_new_packet(sequence):
    packet_type_id = int(sequence[3:6], 2)
    if packet_type_id == 4:
        return get_new_literal(sequence)
    else:
        return get_new_operator(sequence, packet_type_id)


def get_new_operator(sequence, type):
    length_type_id = int(sequence[6], 2)
    if length_type_id == 0:
        size_param = int(sequence[7:22], 2)
        length = 22
    elif length_type_id == 1:
        size_param = int(sequence[7:18], 2)
        length = 18
    return Operator(
        type=type,
        version=int(sequence[0:3], 2),
        size_type=length_type_id,
        size_param=size_param,
        length=length,
    )


def get_new_literal(sequence):
    """type, version, value, length"""
    version = int(sequence[0:3], 2)
    bin_str = ""
    idx = 6

    while sequence[idx] in ["1", "0"]:
        segment = sequence[idx : idx + 5]
        bin_str += segment[1:]
        idx += 5
        if sequence[idx-5] == "0":
            break

    value = int("".join(bin_str), 2)
    return Literal(type=4, version=version, length=idx, value=value)


def parse(bin):
    stack = []
    while len(bin) > 0 and int(bin, 2) > 0:
        new_packet = get_new_packet(bin)
        stack.append(new_packet)
        bin = bin[new_packet.length :]
    return stack


def apply_function(packet, input_packets):
    args = ",".join(str(p.value) for p in input_packets if isinstance(p, Literal))
    new_val = evaluate(f"func{packet.type}({args})")
    new_len = sum(p.length for p in input_packets) + packet.length
    return Literal(type=4, version=0, value=new_val, length=new_len)


def evaluate_functions(stacklist):
    while len(stacklist) > 1:
        new_stack = []
        for idx, packet in enumerate(stacklist):
            applied = False
            if isinstance(packet, Operator):
                cum_len, lit_count = 0, 0
                for idx2, packet2 in enumerate(stacklist[idx + 1 :]):
                    if isinstance(packet2, Literal):
                        cum_len += packet2.length
                        lit_count += 1
                        if (
                            packet.size_type == 0
                            and cum_len == packet.size_param
                            or packet.size_type == 1
                            and lit_count == packet.size_param
                        ):
                            input_packets = stacklist[idx + 1 : idx + idx2 + 2]
                            new = apply_function(packet, input_packets)
                            new_stack.append(new)
                            new_stack.extend(stacklist[idx + idx2 + 2 :])
                            applied = True
                            break
                    else:
                        break
            if applied:
                stacklist = new_stack
                break
            new_stack.append(packet)

    return stacklist[0].value


def evaluate(compstr):
    def func0(*args):
        return sum(args)

    def func1(*args):
        return reduce(lambda a, b: a * b, args)

    def func2(*args):
        return min(args)

    def func3(*args):
        return max(args)

    def func5(*args):
        return int(args[0] > args[1])

    def func6(*args):
        return int(args[0] < args[1])

    def func7(*args):
        return int(args[1] == args[0])

    return eval(compstr)


def solve_1(input_str, mapping):
    binary_str = hex2bin(input_str, mapping)
    parsed = parse(binary_str)
    return sum(packet.version for packet in parsed)


def solve_2(input_str, mapping):
    binary_str = hex2bin(input_str, mapping)
    parsed = parse(binary_str)
    return evaluate_functions(parsed)


if __name__ == "__main__":
    real_input = read_file("data/day_16/input.txt")
    mapping = get_mapping("data/day_16/mapping.txt")

    # Part 1
    assert solve_1("8A004A801A8002F478", mapping) == 16
    assert solve_1("620080001611562C8802118E34", mapping) == 12
    assert solve_1("C0015000016115A2E0802F182340", mapping) == 23
    assert solve_1("A0016C880162017C3686B18A3D4780", mapping) == 31
    assert solve_1(real_input, mapping) == 1014

    # Part 2
    assert solve_2("C200B40A82", mapping) == 3, solve_2("C200B40A82", mapping)
    assert solve_2("04005AC33890", mapping) == 54
    assert solve_2("880086C3E88112", mapping) == 7
    assert solve_2("CE00C43D881120", mapping) == 9
    assert solve_2("D8005AC2A8F0", mapping) == 1
    assert solve_2("F600BC2D8F", mapping) == 0
    assert solve_2("9C005AC2F8F0", mapping) == 0
    assert solve_2("9C0141080250320F1802104A08", mapping) == 1
    assert solve_2(real_input, mapping) == 1922490999789
