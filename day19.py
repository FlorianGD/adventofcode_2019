"""AoC 2019 day 19: Tractor Beam"""

from intcode import Program, read_input
import numpy as np


def scan(program: Program) -> np.array:
    grid = np.zeros((50, 50), dtype=int)
    for x in range(50):
        for y in range(50):
            program.add_input(x)
            program.add_input(y)
            grid[x][y] = next(program.operate())
            program.reset()
    return grid


if __name__ == "__main__":
    puzzle = read_input("./day19_input.txt")
    program = Program(puzzle)
    grid = scan(program)
    print(f"Solution for part 1: {grid.sum()}")
