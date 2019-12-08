"""AoC 2019 day 5: Sunny with a Chance of Asteroids"""

from pathlib import Path
from typing import List
from collections import namedtuple
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
}


def read_input(day: str = "day07_input.txt") -> List[int]:
    puzzle_input = Path(day).read_text()
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


def operate(
    intcodes: List[int], pointer: int, input_: List[int], output: List[int] = []
) -> List[int]:
    instr = get_instruction(intcodes[pointer])
    if instr.opcode == "end":
        return output

    # 1 parameter instructions
    target = intcodes[pointer + 1]

    if instr.opcode == "set_input":
        intcodes[target] = input_.pop()
        return operate(intcodes, pointer + 2, input_, output)

    if instr.opcode == "set_output":
        target = value_from_mode(intcodes, instr.mode1, target)
        output.append(target)
        return operate(intcodes, pointer + 2, input_, output)

    # 2 parameters instructions
    a = value_from_mode(intcodes, instr.mode1, intcodes[pointer + 1])
    b = value_from_mode(intcodes, instr.mode2, intcodes[pointer + 2])
    if instr.opcode == "jump-if-true":
        if a:
            return operate(intcodes, b, input_, output)
        return operate(intcodes, pointer + 3, input_, output)

    if instr.opcode == "jump-if-false":
        if not a:
            return operate(intcodes, b, input_, output)
        return operate(intcodes, pointer + 3, input_, output)
    # 3 parameters instructions
    a = value_from_mode(intcodes, instr.mode1, intcodes[pointer + 1])
    b = value_from_mode(intcodes, instr.mode2, intcodes[pointer + 2])
    target = intcodes[pointer + 3]

    if instr.opcode == "add":
        intcodes[target] = a + b
        return operate(intcodes, pointer + 4, input_, output)

    if instr.opcode == "mul":
        intcodes[target] = a * b
        return operate(intcodes, pointer + 4, input_, output)

    if instr.opcode == "less than":
        if a < b:
            intcodes[target] = 1
            return operate(intcodes, pointer + 4, input_, output)
        else:
            intcodes[target] = 0
            return operate(intcodes, pointer + 4, input_, output)

    if instr.opcode == "equals":
        if a == b:
            intcodes[target] = 1
            return operate(intcodes, pointer + 4, input_, output)
        else:
            intcodes[target] = 0
            return operate(intcodes, pointer + 4, input_, output)

    raise ValueError(f"opcode {instr.opcode} not recognised.")


def run_through(phases, puzzle):
    next_input = [0]
    intcodes = puzzle.copy()
    for i in range(5):
        phase = phases[i]
        next_input.append(phase)
        puzzle = intcodes.copy()
        next_input = operate(puzzle, 0, next_input, [])
    return next_input


def max_of_all_phases(puzzle: List[int]) -> int:
    return max(run_through(phases, puzzle) for phases in permutations(range(5)))[0]


puzzle_test = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
assert max_of_all_phases(puzzle_test) == 43210

print(f"Solution for part 1: {max_of_all_phases(read_input())}")

# Part 2


def operate2(intcodes: List[int], pointer: int, input_: List[int]) -> List[int]:
    output = []
    while True:
        instr = get_instruction(intcodes[pointer])
        if instr.opcode == "end":
            break

        # 1 parameter instructions
        target = intcodes[pointer + 1]

        if instr.opcode == "set_input":
            intcodes[target] = input_.pop()
            pointer += 2
            continue

        if instr.opcode == "set_output":
            target = value_from_mode(intcodes, instr.mode1, target)
            output.append(target)
            pointer += 2
            break

        # 2 parameters instructions
        a = value_from_mode(intcodes, instr.mode1, intcodes[pointer + 1])
        b = value_from_mode(intcodes, instr.mode2, intcodes[pointer + 2])
        if instr.opcode == "jump-if-true":
            if a:
                pointer = b
                continue
            pointer += 3
            continue

        if instr.opcode == "jump-if-false":
            if not a:
                pointer = b
                continue
            pointer += 3
            continue
        # 3 parameters instructions
        a = value_from_mode(intcodes, instr.mode1, intcodes[pointer + 1])
        b = value_from_mode(intcodes, instr.mode2, intcodes[pointer + 2])
        target = intcodes[pointer + 3]

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
                continue
            else:
                intcodes[target] = 0
                pointer += 4
                continue

        if instr.opcode == "equals":
            if a == b:
                intcodes[target] = 1
                pointer += 4
                continue
            else:
                intcodes[target] = 0
                pointer += 4
                continue

        raise ValueError(f"opcode {instr.opcode} not recognised.")
    return output


def run_through2(phases, puzzle):
    next_input = [0]
    intcodes = puzzle.copy()
    for i in range(5):
        phase = phases[i]
        next_input.append(phase)
        puzzle = intcodes.copy()
        next_input = operate2(puzzle, 0, next_input)
    return next_input


def max_of_all_phases2(puzzle: List[int]) -> int:
    return max(run_through2(phases, puzzle) for phases in permutations(range(5)))[0]


puzzle_test = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
assert max_of_all_phases2(puzzle_test) == 43210


def run_through_feedback(phases, puzzle):
    next_input = [0]
    for i in range(5):
        phase = phases[i]
        next_input.append(phase)
        next_input = operate2(puzzle, 0, next_input)
    while True:
        pass
        break
    return next_input


def max_of_all_phases_feedback(puzzle):
    return max(
        run_through_feedback(phases, puzzle) for phases in permutations(range(5, 10))
    )


run_through_feedback([9, 8, 7, 6, 5], read_input())

