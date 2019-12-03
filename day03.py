"""Advent of code day 3: Crossed Wires"""
from typing import List, Tuple, Set, Dict
from pathlib import Path

puzzle: str = Path("day03_input.txt").read_text()


class Wire:
    moves: Dict[str, complex] = {"U": 1j, "D": -1j, "R": 1, "L": -1}

    def __init__(self, directions: List[Tuple[str, int]]):
        self.directions: List[Tuple[str, int]] = directions
        self.path: List[complex] = [0]
        self.positions: Set[complex] = set(self._compute_path())

    def __repr__(self):
        return f"{self.__class__.__name__}(directions={self.directions[:5]},...)"

    def _compute_path(self) -> List[complex]:
        for move, length in self.directions:
            from_ = self.path[-1]
            direction = self.moves[move]
            for i in range(1, length + 1):
                self.path.append(from_ + i * direction)
        return self.path

    def __and__(self, other) -> Set[complex]:
        intersection = self.positions & other.positions
        intersection.remove(0)
        return intersection


def parse_input(puzzle: str) -> List[Wire]:
    directions = [
        [(d[0], int(d[1:])) for d in line.split(",")] for line in puzzle.splitlines()
    ]
    return [Wire(d) for d in directions]


def manhattan_distance(position: complex) -> int:
    return int(abs(position.real) + abs(position.imag))


def first_non_zero_intersection(wire1: Wire, wire2: Wire) -> int:
    # 0 is removed from the intersection
    intersections = wire1 & wire2
    return min([manhattan_distance(p) for p in intersections])


print(f"Solution for part 1: {first_non_zero_intersection(*parse_input(puzzle))}")


def intersection_step(wire1: Wire, wire2: Wire) -> int:
    steps = []
    for intersect in wire1 & wire2:
        for i, p in enumerate(wire1.path):
            if p == intersect:
                break
        for j, p in enumerate(wire2.path):
            if p == intersect:
                break
        steps.append(i + j)
    return min(steps)


print(f"Solution for part 2: {intersection_step(*parse_input(puzzle))}")
