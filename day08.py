"""AoC 2019 day 8: Space Image Format"""

from pathlib import Path
import numpy as np

puzzle: str = Path("./day08_input.txt").read_text().strip()
layers: np.ndarray = np.array(list(puzzle), dtype=int).reshape((-1, 6, 25))

layer_lowest_zeros: int = np.sum(layers == 0, axis=(1, 2)).argmin()

part_one: int = (
    np.sum(layers[layer_lowest_zeros] == 1) * np.sum(layers[layer_lowest_zeros] == 2)
)

print(f"Solution for part 1: {part_one}")

# Part 2

# Below should be the elegant way, but it doesn't work if there are more than 32 arrays
# and we have 100 layers here. It works on the examples though.

# choices = np.argmax(layers != 2, axis=0)
# image = np.choose(choices, layers)

# I'll do it in a not so clean way, and will watch the elegant numpy answer that I could
# not come up with later.

# This gives us the layer with the first value different than 2, i.e. non transparent
selection = (layers != 2).argmax(axis=0)
# We translate that as a triplet of indices using range. This could be improved I guess
indices = [
    (selection[i, j], i, j)
    for i in range(layers.shape[1])
    for j in range(layers.shape[2])
]

image = np.array([layers[i] for i in indices]).reshape((layers.shape[1:]))

# Pretty print
for row in image:
    for col in row:
        if col == 0:
            print(" ", end="")
        else:
            print("█", end="")
    print("\n", end="")
