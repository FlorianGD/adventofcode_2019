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
    display = {0: " ", 1: "█", 2: "#", 3: "=", 4: "o"}
    for y in range(22):
        for x in range(37):
            print(display[grid[(x, y)]], end="")
        print()


def game_p2(program, running_disp=False):
    program.intcodes[0] = 2
    grid = defaultdict(int)
    score = 0
    x_ball = None
    x_bar = None
    while True:
        try:
            x = next(program.operate())
            y = next(program.operate())
            title_id = next(program.operate())
        except StopIteration:
            break
        if x == -1 and y == 0:
            score = title_id
            print(f"score = {score}")
        else:
            grid[(x, y)] = title_id
            if title_id == 3:
                x_bar = x
            elif title_id == 4:
                x_ball = x
        if x_bar is not None and x_ball is not None:
            if x_ball < x_bar:
                program.input.append(-1)
            elif x_ball > x_bar:
                program.input.append(1)
            else:
                program.input.append(0)


if __name__ == "__main__":
    program: Program = Program(puzzle)
    grid: Grid = game(program)
    print(f"Solution for part 1: {Counter(grid.values())[2]}")
    print_grid(grid)

    game_p2(Program(puzzle))
