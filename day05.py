"""AoC 2019 day 5: Sunny with a Chance of Asteroids"""

from pathlib import Path
from typing import List, Tuple
from collections import namedtuple

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
}


def read_input() -> List[int]:
    puzzle_input = Path("./day05_input.txt").read_text()
    return [int(x) for x in puzzle_input.split(",")]


def get_instruction(param: int) -> Instruction:
    opcode = opcodes[param % 100]
    mode1 = "immediate" if param // 100 % 10 else "position"
    mode2 = "immediate" if param // 1000 % 10 else "position"
    mode3 = "immediate" if param // 10000 % 10 else "position"
    return Instruction(opcode, mode1, mode2, mode3)


def value_from_mode(intcodes: List[int], mode: str, val: int) -> int:
    if mode == "position":
        return intcodes[val]
    else:
        return val


def operate(intcodes: List[int], pointer: int = 0, input_: int = 1) -> None:
    instr = get_instruction(intcodes[pointer])
    if instr.opcode == "end":
        return  # intcodes

    # 1 parameter instructions
    target = intcodes[pointer + 1]

    if instr.opcode == "set_input":
        intcodes[target] = input_
        return operate(intcodes, pointer + 2, input_=input_)

    if instr.opcode == "set_output":
        target = value_from_mode(intcodes, instr.mode1, target)
        print(f"output: {target}")
        return operate(intcodes, pointer + 2, input_=input_)

    # 2 parameters instructions
    a = value_from_mode(intcodes, instr.mode1, intcodes[pointer + 1])
    b = value_from_mode(intcodes, instr.mode2, intcodes[pointer + 2])
    if instr.opcode == "jump-if-true":
        if a:
            return operate(intcodes, b, input_)
        return operate(intcodes, pointer + 3, input_)

    if instr.opcode == "jump-if-false":
        if not a:
            return operate(intcodes, b, input_)
        return operate(intcodes, pointer + 3, input_)
    # 3 parameters instructions
    a = value_from_mode(intcodes, instr.mode1, intcodes[pointer + 1])
    b = value_from_mode(intcodes, instr.mode2, intcodes[pointer + 2])
    target = intcodes[pointer + 3]

    if instr.opcode == "add":
        intcodes[target] = a + b
        return operate(intcodes, pointer + 4, input_=input_)

    if instr.opcode == "mul":
        intcodes[target] = a * b
        return operate(intcodes, pointer + 4, input_=input_)

    if instr.opcode == "less than":
        if a < b:
            intcodes[target] = 1
            return operate(intcodes, pointer + 4, input_=input_)
        else:
            intcodes[target] = 0
            return operate(intcodes, pointer + 4, input_=input_)

    if instr.opcode == "equals":
        if a == b:
            intcodes[target] = 1
            return operate(intcodes, pointer + 4, input_=input_)
        else:
            intcodes[target] = 0
            return operate(intcodes, pointer + 4, input_=input_)

    raise ValueError(f"opcode {instr.opcode} not recognised.")


# operate([1002, 4, 3, 4, 33])
puzzle = read_input()
print("part 1")
operate(puzzle, input_=1)

# Part 2
print("part 2")
puzzle = read_input()
operate(puzzle, input_=5)