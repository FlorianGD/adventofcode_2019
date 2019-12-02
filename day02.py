"""Advent of code 2019 Day 2: 1202 Program Alarm"""

from pathlib import Path
from typing import List
from itertools import product


def read_input() -> List[int]:
    puzzle_input = Path("./day02_input.txt").read_text()
    return [int(x) for x in puzzle_input.split(",")]


def operate(intcodes: List[int], position: int = 0) -> List[int]:
    opcode = intcodes[position]
    if opcode == 99:
        return intcodes
    a, b, result_position = intcodes[position + 1 : position + 4]
    if opcode == 1:
        intcodes[result_position] = intcodes[a] + intcodes[b]
        return operate(intcodes, position + 4)
    if opcode == 2:
        intcodes[result_position] = intcodes[a] * intcodes[b]
        return operate(intcodes, position + 4)
    raise ValueError(f"opcode {opcode} not recognised.")


assert operate([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
assert operate([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
assert operate([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
assert operate([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]


def part1(puzzle: List[int]) -> int:
    puzzle[1] = 12
    puzzle[2] = 2
    return operate(puzzle)[0]


puzzle = read_input()
print(f"Solution for part 1: {part1(puzzle)}")


def part2(puzzle: List[int]) -> int:
    for noun, verb in product(range(100), range(100)):
        puzzle2 = puzzle.copy()
        puzzle2[1] = noun
        puzzle2[2] = verb
        if operate(puzzle2)[0] == 19690720:
            return 100 * noun + verb
    raise ValueError("Pair not found, surely a mistake in the code.")


puzzle = read_input()
print(f"Solution for part 1: {part2(puzzle)}")
