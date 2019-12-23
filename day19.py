"""AoC 2019 day 19: Tractor Beam"""

from intcode import Program, read_input
import numpy as np
from typing import Tuple


def scan(program: Program, shape: Tuple[int, int] = (50, 50)) -> np.array:
    grid = np.zeros(shape, dtype=int)
    for x in range(shape[0]):
        for y in range(shape[1]):
            program.add_input(x)
            program.add_input(y)
            grid[x][y] = next(program.operate())
            program.reset()
    return grid


def test_corners(program: Program, x: int, y: int) -> bool:
    for xx, yy in [(x, y), (x + 99, y), (x, y + 99), (x + 99, y + 99)]:
        program.reset()
        program.add_input(xx)
        program.add_input(yy)
        if next(program.operate()) != 1:
            return False
    return True


def part2(program: Program) -> Tuple[int, int]:
    # values below found graphically
    for x in range(800, 1100):
        for y in range(200, 500):
            if test_corners(program, x, y):
                return x, y
    raise ValueError("not found")


if __name__ == "__main__":
    puzzle = read_input("./day19_input.txt")
    program = Program(puzzle)
    grid = scan(program)
    print(f"Solution for part 1: {grid.sum()}")
    # I mixed up x and y somehow
    x, y = part2(program)
    print(f"Solution for part 2: {y*10000 + x}")
