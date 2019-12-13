"""AoC 2019 day 13: Care Package"""
from collections import Counter, defaultdict
from typing import DefaultDict, List, Tuple

from day09 import Program, read_input

Grid = DefaultDict[Tuple[int, int], int]
puzzle = read_input("./day13_input.txt")


def game(program: Program) -> Grid:
    grid: Grid = defaultdict(int)
    while True:
        try:
            x = next(program.operate())
            y = next(program.operate())
            title_id = next(program.operate())
        except StopIteration:
            return grid
        grid[(x, y)] = title_id


def print_grid(grid: Grid) -> None:
    display = {0: " ", 1: "█", 2: "#", 3: "―", 4: "🌑"}
    for y in range(22):
        for x in range(37):
            print(display[grid[(x, y)]], end="")
        print()


if __name__ == "__main__":
    program: Program = Program(puzzle)
    grid: Grid = game(program)
    print(f"Solution for part 1: {Counter(grid.values())[2]}")
    print_grid(grid)
