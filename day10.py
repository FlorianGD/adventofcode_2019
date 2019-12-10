"""AoC 2019 day 10: Monitoring Station"""
from typing import List, Tuple, Generator, Set, Dict
from pathlib import Path

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
    results = {}
    for a in coordinates:
        masked_coord: Set = set()
        for b in coordinates - {a}:
            if b in masked_coord:
                continue
            for c in coordinates - {a, b}:
                if c in masked_coord:
                    continue
                if masked(a, b, c):
                    # results[a] -= 1
                    masked_coord.add(farthest(a, b, c))
        results[a] = len(coordinates - {a} - masked_coord)
    return results


# example = """.#..#
# .....
# #####
# ....#
# ...##"""

# assert max(visibles(example).values()) == 8


# example2 = """......#.#.
# #..#.#....
# ..#######.
# .#.#.###..
# .#..#.....
# ..#....#.#
# #..#....#.
# .##.#..###
# ##...#..#.
# .#....####"""

# assert max(visibles(example2).values()) == 33

# example3 = """#.#...#.#.
# .###....#.
# .#....#...
# ##.#.#.#.#
# ....#.#.#.
# .##..###.#
# ..#...##..
# ..##....##
# ......#...
# .####.###."""
# assert max(visibles(example3).values()) == 35

# example4 = """.#..#..###
# ####.###.#
# ....###.#.
# ..###.##.#
# ##.##.#.#.
# ....###..#
# ..#.#..#.#
# #..#.#.###
# .##...##.#
# .....#.#.."""
# assert max(visibles(example4).values()) == 41

# example5 = """.#..##.###...#######
# ##.############..##.
# .#.######.########.#
# .###.#######.####.#.
# #####.##.#.##.###.##
# ..#####..#.#########
# ####################
# #.####....###.#.#.##
# ##.#################
# #####.##.###..####..
# ..######..##.#######
# ####.##.####...##..#
# .#####..#.######.###
# ##...#.##########...
# #.##########.#######
# .####.#.###.###.#.##
# ....##.##.###..#####
# .#.#.###########.###
# #.#.#.#####.####.###
# ###.##.####.##.#..##"""

# ex5 = visibles(example5)
# assert max(ex5.values()) == 210

puzzle = Path("./day10_input.txt").read_text()
print(f"Solution for part 1: {max(visibles(puzzle).values())}")
