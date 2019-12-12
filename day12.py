"""AoC 2019 day 12: The N-Body Problem"""
import numpy as np
import re
from typing import Tuple


def parse_puzzle(puzzle: str) -> Tuple[np.array, np.array]:
    moons = [re.findall(r"-?\d+", line) for line in puzzle.splitlines()]
    positions = np.array(moons, dtype=int)
    return positions, np.zeros_like(positions)


def apply_grav(pos: np.array, velo: np.array) -> np.array:
    return np.array([np.sum(np.sign(pos - pos[i]), axis=0) for i in range(4)])


def simulate(pos: np.array, velo: np.array):
    velo += apply_grav(pos, velo)
    pos += velo


def energy(pos: np.array, velo: np.array) -> int:
    return np.sum(np.sum(np.abs(pos), axis=1) * np.sum(np.abs(velo), axis=1))


puzzle = """<x=14, y=15, z=-2>
<x=17, y=-3, z=4>
<x=6, y=12, z=-13>
<x=-2, y=10, z=-8>"""

if __name__ == "__main__":
    positions, velocities = parse_puzzle(puzzle)
    for _ in range(1000):
        simulate(positions, velocities)
    print(f"Solution for part 1: {energy(positions, velocities)}")
