"""Advent of code 2019 day 1: The Tyranny of the Rocket Equation"""
from typing import List, Union

with open("./day01_input.txt") as f:
    puzzle = f.readlines()


def compute_fuel(mass: Union[str, int]) -> int:
    return int(mass) // 3 - 2


def part1(puzzle: List[str]) -> int:
    total = 0
    for mass in puzzle:
        total += compute_fuel(mass)
    return total


print(f"Day 1 Part 1 solution: {part1(puzzle)}")


def part2(puzzle: List[str]) -> int:
    total = 0
    for mass in puzzle:
        current = compute_fuel(mass)
        while current > 0:
            total += current
            current = compute_fuel(current)
    return total


print(f"Day 1 Part 3 solution: {part2(puzzle)}")
