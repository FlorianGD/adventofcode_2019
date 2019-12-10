"""AoC 2019 day 10: Monitoring Station"""
import numpy as np
from typing import List, Tuple, Generator, Set, Dict
from itertools import combinations
import pandas as pd
from collections import defaultdict

Coord = Tuple[int, int]


def get_asteroids_coordinates(puzzle: str) -> Generator[Coord, None, None]:
    for j, row in enumerate(puzzle.splitlines()):
        for i, val in enumerate(row):
            if val == "#":
                yield (i, j)


def masked(p1: Coord, p2: Coord, p3: Coord) -> bool:
    """True if p2 or p3 cannot be seen from p1."""
    p1x, p1y, p2x, p2y, p3x, p3y = (*p1, *p2, *p3)
    if (p2x - p1x) * (p3y - p1y) - (p2y - p1y) * (p3x - p1x) != 0:
        return False
    return (p2x - p1x) * (p3x - p1x) + (p2y - p1y) * (p3y - p1y) > 0


def farthest(p1: Coord, p2: Coord, p3: Coord) -> Coord:
    """which of p2 or p3 is farthest to p1?"""
    p1x, p1y, p2x, p2y, p3x, p3y = (*p1, *p2, *p3)
    d2 = abs(p2x - p1x) + abs(p2y - p1y)
    d3 = abs(p3x - p1x) + abs(p3y - p1y)
    return p2 if max(d2, d3) == d2 else p3


def visibles(puzzle: str) -> Dict[Coord, int]:
    coordinates = set(get_asteroids_coordinates(puzzle))
    max_possible = len(coordinates) - 1
    results = defaultdict(lambda: max_possible)
    for a in coordinates:
        burnt: Set = set()
        for b in coordinates - {a}:
            if b in burnt:
                continue
            for c in coordinates - {a, b}:
                if c in burnt:
                    continue
                if masked(a, b, c):
                    results[a] -= 1
                    burnt.add(farthest(a, b, c))
    return results


example = """.#..#
.....
#####
....#
...##"""

assert max(visibles(example).values()) == 8


example2 = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

assert max(visibles(example2).values()) == 33

example3 = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""
assert max(visibles(example3).values()) == 35

example4 = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""
assert max(visibles(example4).values()) == 41

example5 = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

ex5 = visibles(example5)
assert max(ex5.values()) == 210
