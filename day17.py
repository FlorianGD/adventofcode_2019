"""AoC 2019: day17 Set and Forget"""
import numpy as np
from intcode import Program, read_input


def get_ascii(program: Program) -> str:
    grid = []
    while True:
        try:
            grid.append(chr(next(program.operate())))
        except StopIteration:
            break
    return "".join(grid)


def create_grid(ascii: str) -> np.array:
    grid = np.zeros((len(ascii.splitlines()), len(ascii.splitlines()[0])), dtype=str)
    for i, line in enumerate(ascii.splitlines()):
        for j, val in enumerate(line):
            grid[i][j] = val
    return grid


def compute_intersections_value(grid: np.array) -> int:
    total = 0
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            if (
                grid[i][j] == "#"
                and grid[i + 1][j] == "#"
                and grid[i - 1][j] == "#"
                and grid[i][j + 1] == "#"
                and grid[i][j - 1] == "#"
            ):
                total += i * j
    return total


if __name__ == "__main__":
    program = Program(read_input("./day17_input.txt"))
    ascii = get_ascii(program)
    grid = create_grid(ascii)

    print(f"Solution for part 1:{compute_intersections_value(grid)}")
