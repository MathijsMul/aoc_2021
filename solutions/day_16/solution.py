import os
from collections import defaultdict, Counter
import numpy as np
from functools import reduce


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return open(input_path).read()
    # return [line.strip().split("-") for line in open(input_path).readlines()]


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


def sum_versions(decoded):
    if len(decoded) == 2:
        return decoded[0]
    elif len(decoded) > 2:
        return decoded[0] + sum(sum_versions(packet) for packet in decoded[2:])


def traverse(bin):
    packet_conditions = []
    subpacket_count = 0
    len_count = 0
    versions = []
    segments = []
    stack = []

    while len(bin) > 0:
        if int(bin, 2) == 0:
            break
        if stack:
            _, op_type, op_param, _, _ = next(
                filter(lambda packet: packet[0] == "op", stack[::-1])
            )
            if (op_type == "len" and op_param == len_count) or (
                op_type == "num" and op_param == subpacket_count
            ):
                subpacket_count, len_count = 0, 0
                # stack.pop()

        if not packet_conditions or packet_conditions[-1][0] == "op":
        # elif not stack or stack[-1][0] == "op":
            packet_version = int(bin[0:3], 2)
            versions.append(packet_version)
            packet_type_id = int(bin[3:6], 2)
            if packet_type_id == 4:
                # literal
                packet_conditions.append("lit")
                stack.append(("lit"))
                bin = bin[6:]
            else:
                # operator
                length_type_id = int(bin[6])
                if length_type_id == 0:
                    length = int(bin[7:22], 2)
                    bin = bin[22:]
                    stack.append(("op", "len", length, packet_type_id, 22))
                elif length_type_id == 1:
                    num_subpackets = int(bin[7:18], 2)
                    bin = bin[18:]
                    stack.append(("op", "num", num_subpackets, packet_type_id, 18))
        else:
            segment = bin[:5]
            len_count += len(segment)
            segments.append(segment)
            if segment[0] == "0":
                # final five bits of literal
                packet_conditions.pop()
                stack.pop()
                subpacket_count += 1
                len_count += 6  # for literal headers
                binary_segment = "".join(segments)
                segment_val = int(binary_segment, 2)

                stack.append(("lit", segment_val, len(binary_segment) + 6))
                segments = []
            bin = bin[5:]

        # breakpoint()

    # part 1
    # return sum(versions)
    return evaluate_functions(stack), sum(versions)


def solve_1(input_str, mapping):
    binary_str = hex2bin(input_str, mapping)
    value, version_sum = traverse(binary_str)
    return version_sum


def solve_2(input_str, mapping):
    binary_str = hex2bin(input_str, mapping)
    value, version_sum = traverse(binary_str)
    return value


def evaluate_functions(stacklist):
    print(stacklist)
    a = list(stacklist)
    total = sum(i[-1] for i in stacklist)

    while len(stacklist) > 1:
        assert sum(i[-1] for i in stacklist) == total
        # if len(stacklist) < 60:
        #     breakpoint()

        new_stack = []
        for idx, packet in enumerate(stacklist):
            applied = False
            if packet[0] == "op":
                if packet[1] == "len":
                    length = packet[2]
                    cum_len = 0
                    for idx2, packet2 in enumerate(stacklist[idx + 1 :]):
                        if packet2[0] == "lit":
                            cum_len += packet2[2]
                            if cum_len == length:
                                print(f"Length match: {cum_len} = {length}")
                                input_packets = stacklist[idx + 1 : idx + idx2 + 2]
                                args = ",".join(
                                    str(p[1]) for p in input_packets if p[0] == "lit"
                                )
                                assert sum(p[2] for p in input_packets) == cum_len

                                compstr = f"func{packet[3]}({args})"
                                print(f"Input: {input_packets}")

                                new_val = evaluate(compstr)
                                new_len = sum(p[-1] for p in input_packets) + packet[-1]
                                newpacket = ("lit", new_val, new_len)
                                new_stack.append(newpacket)
                                new_stack.extend(stacklist[idx + idx2 + 2 :])
                                assert len(new_stack) == len(stacklist) - len(
                                    input_packets
                                )
                                applied = True
                                break
                        else:
                            break
                elif packet[1] == "num":
                    num = packet[2]
                    lit_count = 0
                    for idx2, packet2 in enumerate(stacklist[idx + 1 :]):
                        if packet2[0] == "lit":
                            lit_count += 1
                            if lit_count == num:
                                input_packets = stacklist[idx + 1 : idx + idx2 + 2]
                                assert len(input_packets) == num
                                print(f"Num match: {num} = {len(input_packets)}")

                                args = ",".join(
                                    str(p[1]) for p in input_packets if p[0] == "lit"
                                )
                                compstr = f"func{packet[3]}({args})"
                                print(f"Input: {input_packets}")
                                new_val = evaluate(compstr)
                                new_len = sum(p[-1] for p in input_packets) + packet[-1]
                                newpacket = ("lit", new_val, new_len)
                                new_stack.append(newpacket)
                                new_stack.extend(stacklist[idx + idx2 + 2 :])
                                assert len(new_stack) == len(stacklist) - len(
                                    input_packets
                                )

                                applied = True
                                break
                        else:
                            break
            if applied:
                print(f"Added {newpacket}")
                stacklist = new_stack
                break
            else:
                new_stack.append(packet)

    print(stacklist)
    assert stacklist[0][-1] == total
    return stacklist[0][1]


def evaluate(compstr):
    def func0(*args):
        print(f"Summing {args} gives: {sum(args)}")
        return sum(args)

    def func1(*args):
        print(f"Multiplying {args} gives: {reduce(lambda a, b: a * b, args)}")
        return reduce(lambda a, b: a * b, args)

    def func2(*args):
        print(f"Min of {args}: {min(args)}")

        return min(args)

    def func3(*args):
        print(f"Max of {args}: {max(args)}")
        return max(args)

    def func5(*args):
        print(f"Is {args[0]} greater than {args[1]}?")
        print(int(args[0] > args[1]))

        assert len(args) == 2
        return int(args[0] > args[1])

    def func6(*args):
        print(f"Is {args[0]} smaller than {args[1]}?")
        print(int(args[0] < args[1]))
        assert len(args) == 2

        return int(args[0] < args[1])

    def func7(*args):
        print(f"Is {args[1]} equal to {args[0]}?")
        print(int(args[1] == args[0]))
        assert len(args) == 2
        return int(args[1] == args[0])

    print(compstr)
    return eval(compstr)


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
    assert solve_2("C200B40A82", mapping) == 3
    assert solve_2("04005AC33890", mapping) == 54
    assert solve_2("880086C3E88112", mapping) == 7
    assert solve_2("CE00C43D881120", mapping) == 9
    assert solve_2("D8005AC2A8F0", mapping) == 1
    assert solve_2("F600BC2D8F", mapping) == 0
    assert solve_2("9C005AC2F8F0", mapping) == 0
    assert solve_2("9C0141080250320F1802104A08", mapping) == 1

    print(solve_2(real_input, mapping))
    # 2258651371210461 too high
