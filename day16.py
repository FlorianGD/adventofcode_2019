"""AoC 2019: day 16 Flawed Frequency Transmission"""
from functools import reduce
from operator import add
from itertools import cycle, repeat, chain
from typing import Generator, List, Iterator
from pathlib import Path
import numpy as np

pattern: List[int] = [0, 1, 0, -1]


def phase(index: int, pattern: List[int] = pattern) -> Iterator[int]:
    p = cycle(chain.from_iterable(repeat(i, index) for i in pattern))
    next(p)
    return p


def operate(signal: List[int], phase: Iterator[int]) -> int:
    result = reduce(add, (a * b for a, b in zip(signal, phase)))
    return int(str(result)[-1])


def fft(puzzle: str, n: int = 100) -> List[int]:
    signal = list(map(int, list(puzzle)))
    for _ in range(n):
        signal = [operate(signal, phase(i)) for i in range(1, len(signal) + 1)]
    return signal


def part2(puzzle: str) -> str:
    # the offset is after the middle of the matrix, so we only have 0 and 1 in the phase
    # and the digits only depend on the sum of the preceding digits
    offset = int(puzzle[:7])
    signal = list(map(int, list(puzzle * 10000)))[offset:]
    rev_signal = np.fromiter(reversed(signal), dtype=int)

    for _ in range(100):
        rev_signal = np.cumsum(rev_signal) % 10
    return "".join(str(i) for i in reversed(rev_signal[-8:]))


if __name__ == "__main__":
    puzzle = Path("./day16_input.txt").read_text().strip()
    print(f"Solution for part 1: {''.join(str(i) for i in fft(puzzle)[:8])}")
    print(f"Solution for part 2: {part2(puzzle)}")
