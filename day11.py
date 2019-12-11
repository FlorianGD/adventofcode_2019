"""AoC 2019 day 11: Space Police"""

from day09 import Program
from collections import defaultdict
from typing import DefaultDict, Dict, List
from pathlib import Path

moves: Dict[str, complex] = {"U": 1j, "D": -1j, "R": 1, "L": -1}
turn_left = {"U": "L", "L": "D", "D": "R", "R": "U"}
turn_right = {"U": "R", "R": "D", "D": "L", "L": "U"}
turns = [turn_left, turn_right]


def paint(program: Program, start: int = 0) -> DefaultDict[complex, int]:
    """Returns a dict of complex coordinates with the painting value."""
    position: complex = 0
    direction = "U"
    areas: DefaultDict[complex, int] = defaultdict(int)
    areas[position] = start
    program.pointer = 0
    while True:
        program.input = [areas[position]]
        try:
            color = next(program.operate())
            turn = next(program.operate())
        except StopIteration:
            break
        areas[position] = color
        direction = turns[turn][direction]
        position += moves[direction]
    return areas


def display(areas: DefaultDict[complex, int]):
    for row in range(1, -7, -1):
        for col in range(43):
            if areas[complex(col, row)] == 1:
                print("█", end="")
            else:
                print(" ", end="")
        print("\n", end="")


if __name__ == "__main__":
    puzzle: List[int] = [int(x) for x in Path("day11_input.txt").read_text().split(",")]
    program = Program(puzzle)
    areas = paint(program)
    print(f"Solution for part 1: {len(areas)}")

    areas2 = paint(program, 1)
    display(areas2)
