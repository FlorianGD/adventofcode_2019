"""AoC 2019 day 10: Monitoring Station"""
import cmath
from pathlib import Path
from typing import Dict, Generator, List, Set, Tuple

Coord = Tuple[int, int]


def get_asteroids_coordinates(puzzle: str) -> Generator[Coord, None, None]:
    for j, row in enumerate(puzzle.splitlines()):
        for i, val in enumerate(row):
            if val == "#":
                yield (i, j)


def masked(p1: Coord, p2: Coord, p3: Coord) -> bool:
    """True if p2 or p3 cannot be seen from p1."""
    p1x, p1y, p2x, p2y, p3x, p3y = *p1, *p2, *p3  # type: ignore
    if (p2x - p1x) * (p3y - p1y) - (p2y - p1y) * (p3x - p1x) != 0:  # type: ignore
        return False
    return (p2x - p1x) * (p3x - p1x) + (p2y - p1y) * (p3y - p1y) > 0  # type: ignore


def farthest(p1: Coord, p2: Coord, p3: Coord) -> Coord:
    """which of p2 or p3 is farthest to p1?"""
    p1x, p1y, p2x, p2y, p3x, p3y = *p1, *p2, *p3  # type: ignore
    d2 = abs(p2x - p1x) + abs(p2y - p1y)  # type: ignore
    d3 = abs(p3x - p1x) + abs(p3y - p1y)  # type: ignore
    return p2 if max(d2, d3) == d2 else p3


def visibles(puzzle: str) -> Dict[Coord, Set[Coord]]:
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
        results[a] = coordinates - {a} - masked_coord
    return results


def sort_by_angle(center: Coord, coordinates: Set[Coord]) -> List[Coord]:
    pi = cmath.pi
    complex_center = complex(*center)
    coords = list(coordinates)
    centered_complex_coord = [complex(*coord) - complex_center for coord in coords]
    phases = [(cmath.phase(c) + pi / 2) % (2 * pi) for c in centered_complex_coord]
    coordinates_by_phase = sorted(zip(phases, coords))
    return [coord for _, coord in coordinates_by_phase]


if __name__ == "__main__":
    puzzle = Path("./day10_input.txt").read_text()
    all_visibles = visibles(puzzle)
    print(f"Solution for part 1: {max(map(len, all_visibles.values()))}")
    center_coord = max(all_visibles.items(), key=lambda x: len(x[1]))[0]
    by_angle = sort_by_angle(center_coord, all_visibles[center_coord])
    solution = by_angle[199]
    print(f"Solution for part 2: {solution[0] * 100 + solution[1]}")
