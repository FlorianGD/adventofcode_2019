"""AoC 2019 day 8: Space Image Format"""

from typing import List
from pathlib import Path
import numpy as np

puzzle: str = Path("./day08_input.txt").read_text().strip()
layers: np.ndarray = np.array(list(puzzle), dtype=int).reshape((-1, 6, 25))

layer_lowest_zeros: int = np.sum(layers == 0, axis=(1, 2)).argmin()

part_one: int = (
    np.sum(layers[layer_lowest_zeros] == 1) * np.sum(layers[layer_lowest_zeros] == 2)
)

print(f"Solution for part 1: {part_one}")
