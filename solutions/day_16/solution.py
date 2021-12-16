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


# def get_version_nr(bin_packet):
#     version_bits = bin_packet[:3]
#     return int(version_bits, 2)

#
# def decode(bin_message):
#     packet_version = int(bin_message[:3], 2)
#     packet_type_id = int(bin_message[3:6], 2)
#     if packet_type_id == 4:
#         # literal
#         return (packet_version, packet_type_id)
#     else:
#         # operator
#         length_type_id = bin_message[6]
#         if length_type_id == "0":
#             # The next 15 bits are a number that represents the total length in bits of the
#             # sub-packets contained by this packet.
#             total_length = int(bin_message[7:22], 2)
#             subpackets = get_subpackets(bin_message[22:22+total_length], None)
#
#             return (packet_version, packet_type_id, [decode(subp) for subp in subpackets])
#             # for idx, char in enumerate(bin_message[22:22+total_length]):
#
#         elif length_type_id == "1":
#             # The next 11 bits are a number that represents the number of sub-packets immediately
#             # contained by this packet.
#             num_subpackets = int(bin_message[7:18], 2)
#             if num_subpackets == 1:
#                 return (packet_version, packet_type_id, decode(bin_message[18:]))
#             else:
#                 # parse subpackets
#                 subpackets = get_subpackets(bin_message[18:], num_subpackets)
#                 return (packet_version, packet_type_id, [decode(subp) for subp in subpackets])
#
#
# def get_subpackets(sequence, num):
#     subpackets = []
#     while len(sequence) > 3:
#         packet_type_id = int(sequence[3:6], 2)
#         if packet_type_id == 4:
#             # literal
#             ...
#             bit_idx = 6
#             while sequence[bit_idx] in ["0", "1"]:
#                 bits = sequence[bit_idx + 5 * bit_idx: bit_idx + 5 * (1 + bit_idx)]
#                 if sequence[bit_idx] == "0":
#                     subpacket = sequence[:bit_idx + 5 * (1 + bit_idx)]
#                     subpackets.append(subpacket)
#                     sequence = sequence[bit_idx + 5 * (1 + bit_idx):]
#                     break
#
#         else:
#             # operator
#             length_type_id = sequence[6]
#             if length_type_id == "0":
#                 # The next 15 bits are a number that represents the total length in bits of the
#                 # sub-packets contained by this packet.
#                 subpacket = sequence[7:22]
#                 subpackets.append(subpacket)
#                 sequence = sequence[22:]
#             elif length_type_id == "1":
#                 num_subpackets = int(sequence[7:18], 2)
#                 subsubpackets = get_subpackets(sequence[18:], num_subpackets)
#                 subpackets.extend(subsubpackets)
#                 sequence = ""
#
#     return subpackets


def sum_versions(decoded):
    if len(decoded) == 2:
        return decoded[0]
    elif len(decoded) > 2:
        return decoded[0] + sum(sum_versions(packet) for packet in decoded[2:])


def solve_1(hex_message, mapping):
    bin_message = hex2bin(hex_message, mapping)
    # version = get_version_nr(bin_message)
    # return version
    # decoded = decode(bin_message)
    # return sum_versions(decoded)


def solve_2(input_list):
    return


def traverse(bin):
    packet_conditions = []
    processed = []
    subpacket_count = 0
    len_count = 0
    versions = []
    value = 0
    segments = []
    stack = []
    compstring = ""

    while len(bin) > 0 or len(packet_conditions) > 0:
        if int(bin, 2) == 0:
            compstring += ")"
            bin = ""
            packet_conditions.pop()
            break
        if not packet_conditions or packet_conditions[-1][0] == "op":
            if packet_conditions and packet_conditions[-1][0] == "op":
                if (
                    packet_conditions[-1][1] == "len"
                    and len_count == packet_conditions[-1][2]
                ) or (
                    packet_conditions[-1][1] == "num"
                    and subpacket_count == packet_conditions[-1][2]
                ):

                    comp_type = packet_conditions[-1][3]
                    # if comp_type == 0:
                    #     # sum
                    #     val = sum(stack)
                    # elif comp_type == 1:
                    #     # product
                    #     val = reduce(lambda a, b: a * b, stack)
                    # elif comp_type == 2:
                    #     # min
                    #     val = min(stack)
                    # elif comp_type == 3:
                    #     # max
                    #     val = max(stack)
                    # elif comp_type == 5:
                    #     # greater than
                    #     val = int(stack[1] < stack[0])
                    # elif comp_type == 6:
                    #     # less than
                    #     val = int(stack[1] > stack[0])
                    # elif comp_type == 7:
                    #     # equal to
                    #     val = int(stack[1] == stack[0])

                    # stack = [val]
                    compstring += "),"
                    packet_conditions.pop()
                    subpacket_count, len_count = 0, 0
                if len(packet_conditions) == 0:
                    compstring += "),"
                    break


            packet_version = int(bin[0:3], 2)
            versions.append(packet_version)
            packet_type_id = int(bin[3:6], 2)
            if packet_type_id == 4:
                # literal
                packet_conditions.append("lit")
                processed.append("lit")

                bin = bin[6:]
            else:
                # operator
                length_type_id = int(bin[6])
                compstring += f"func{packet_type_id}("

                if length_type_id == 0:
                    length = int(bin[7:22], 2)
                    bin = bin[22:]
                    packet_conditions.append(("op", "len", length, packet_type_id))
                    processed.append(("op", "len", length, packet_type_id))

                elif length_type_id == 1:
                    num_subpackets = int(bin[7:18], 2)
                    bin = bin[18:]
                    packet_conditions.append(
                        ("op", "num", num_subpackets, packet_type_id)
                    )
                    processed.append(
                        ("op", "num", num_subpackets, packet_type_id)
                    )

        else:
            segment = bin[:5]
            len_count += len(segment)
            segments.append(segment)
            if segment[0] == "0":
                # final five bits of literal
                packet_conditions.pop()
                subpacket_count += 1
                len_count += 6  # for literal headers

                segment_val = int("".join(segments), 2)
                stack.append(segment_val)
                compstring += str(segment_val) + ","
                segments = []
            bin = bin[5:]

        # breakpoint()

    # part 1
    # return sum(versions)
    return sum(versions), stack, compstring


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
        return int(args[1] < args[0])

    def func6(*args):
        return int(args[1] > args[0])

    def func7(*args):
        return int(args[1] == args[0])

    return eval(compstr)


if __name__ == "__main__":
    real_input = read_file("data/day_16/input.txt")
    mapping = get_mapping("data/day_16/mapping.txt")

    # Part 1
    # bin = hex2bin("8A004A801A8002F478", mapping)
    # assert traverse(bin)[0] == 16
    #
    # bin = hex2bin("620080001611562C8802118E34", mapping)
    # assert traverse(bin)[0] == 12
    #
    # bin = hex2bin("C0015000016115A2E0802F182340", mapping)
    # assert traverse(bin)[0] == 23
    #
    # bin = hex2bin("A0016C880162017C3686B18A3D4780", mapping)
    # assert traverse(bin)[0] == 31
    #
    # realbin = hex2bin(real_input, mapping)
    # assert traverse(realbin)[0] == 1014

    # Part 2
    # realbin = hex2bin("C200B40A82", mapping)
    # print(traverse(realbin)[2])
    # assert evaluate(traverse(realbin)[2]) == 3
    #
    # realbin = hex2bin("04005AC33890", mapping)
    # print(traverse(realbin)[2])
    # assert evaluate(traverse(realbin)[2]) == 54
    #
    # realbin = hex2bin("880086C3E88112", mapping)
    # print(traverse(realbin)[2])
    # assert evaluate(traverse(realbin)[2]) == 7
    #
    # realbin = hex2bin("CE00C43D881120", mapping)
    # print(traverse(realbin)[2])
    # assert evaluate(traverse(realbin)[2]) == 9
    #
    # realbin = hex2bin("D8005AC2A8F0", mapping)
    # print(traverse(realbin)[2])
    # assert evaluate(traverse(realbin)[2]) == 1, evaluate(traverse(realbin)[2])
    #
    # realbin = hex2bin("F600BC2D8F", mapping)
    # assert evaluate(traverse(realbin)[2]) == 0
    #
    # realbin = hex2bin("9C005AC2F8F0", mapping)
    # assert evaluate(traverse(realbin)[2]) == 0

    realbin = hex2bin("9C0141080250320F1802104A08", mapping)
    print(traverse(realbin)[2])
    # assert evaluate(traverse(realbin)[2] + ")") == 1, traverse(realbin)[2]
    assert evaluate(traverse(realbin)[2]) == 1, traverse(realbin)[2]

    realbin = hex2bin(real_input, mapping)
    # print(traverse(realbin)[2] + 95 * ")")
    # print(evaluate(traverse(realbin)[2] + 95 * ")"))

