"""AoC 2019 day 9: Sensor Boost"""

from pathlib import Path
from typing import List, Generator, Tuple, Dict, DefaultDict
from collections import namedtuple, defaultdict
from itertools import permutations

Instruction = namedtuple("Instruction", "opcode mode1 mode2 mode3")

opcodes = {
    99: "end",
    1: "add",
    2: "mul",
    3: "set_input",
    4: "set_output",
    5: "jump-if-true",
    6: "jump-if-false",
    7: "less than",
    8: "equals",
    9: "adjust_base",
}

Intcodes = DefaultDict[int, int]


def make_intcodes(puzzle: List[int]) -> Intcodes:
    intcodes: Intcodes = defaultdict(int)
    for i, val in enumerate(puzzle):
        intcodes[i] = val
    return intcodes


def read_input(day: str = "day09_input.txt") -> Intcodes:
    puzzle_input = Path(day).read_text()
    puzzle = [int(x) for x in puzzle_input.split(",")]
    return make_intcodes(puzzle)


def get_instruction(param: int, opcodes: Dict[int, str] = opcodes) -> Instruction:
    opcode = opcodes[param % 100]
    modes = {0: "position", 1: "immediate", 2: "relative"}
    mode1 = modes[param // 100 % 10]
    mode2 = modes[param // 1000 % 10]
    mode3 = modes[param // 10000 % 10]
    return Instruction(opcode, mode1, mode2, mode3)


def value_from_mode(intcodes: Intcodes, mode: str, val: int, base: int) -> int:
    if mode == "position":
        return intcodes[val]
    elif mode == "immediate":
        return val
    elif mode == "relative":
        return intcodes[base + val]
    else:
        raise ValueError(f"Not recognized mode: {mode}.")


def operate(
    intcodes: Intcodes, input_: List[int], pointer: int = 0
) -> Generator[Tuple[int, int], None, None]:
    """yields the output and the pointer for a given program."""
    base = 0
    while True:
        instr = get_instruction(intcodes[pointer])
        if instr.opcode == "end":
            return

        # 1 parameter instructions
        if instr.opcode == "set_input":
            target = intcodes[pointer + 1]
            if instr.mode1 == "relative":
                target += base
            intcodes[target] = input_.pop()
            pointer += 2
            continue
        
        a = value_from_mode(intcodes, instr.mode1, intcodes[pointer + 1], base)
        if instr.opcode == "set_output":
            pointer += 2
            yield a, pointer
            continue

        if instr.opcode == "adjust_base":
            base += a
            pointer += 2
            continue

        # 2 parameters instructions
        # a defined above
        b = value_from_mode(intcodes, instr.mode2, intcodes[pointer + 2], base)
        if instr.opcode == "jump-if-true":
            if a:
                pointer = b
            else:
                pointer += 3
            continue

        if instr.opcode == "jump-if-false":
            if not a:
                pointer = b
            else:
                pointer += 3
            continue
        # 3 parameters instructions
        # a, b defined above already
        target = intcodes[pointer + 3]
        if instr.mode3 == "relative":
            target += base
        # target = value_from_mode(intcodes, instr.mode3, intcodes[pointer + 3], base)

        if instr.opcode == "add":
            intcodes[target] = a + b
            pointer += 4
            continue

        if instr.opcode == "mul":
            intcodes[target] = a * b
            pointer += 4
            continue

        if instr.opcode == "less than":
            if a < b:
                intcodes[target] = 1
                pointer += 4
            else:
                intcodes[target] = 0
                pointer += 4
            continue

        if instr.opcode == "equals":
            if a == b:
                intcodes[target] = 1
                pointer += 4
            else:
                intcodes[target] = 0
                pointer += 4
            continue

        raise ValueError(f"opcode {instr.opcode} not recognised.")


# puzzle_test = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
# print(list(a for a, b in operate(make_intcodes(puzzle_test), [])))

# puzzle_test = [104, 1125899906842624, 99]
# print(list(operate(make_intcodes(puzzle_test), [])))

# puzzle_test = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
# print(list(operate(make_intcodes(puzzle_test), [])))

print("Solution for part 1:", end="")
print(next(a for a, b in operate(read_input(), [1])))

# Part 2
print("Solution for part 2:", end="")
print(next(a for a, b in operate(read_input(), [2])))
