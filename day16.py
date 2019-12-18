"""AoC 2019: day 16 Flawed Frequency Transmission"""
from functools import reduce
from operator import add
from itertools import cycle, repeat, chain
from typing import Generator, List, Tuple, Iterator
from pathlib import Path

pattern: List[int] = [0, 1, 0, -1]


def phase(index: int, pattern: List[int] = pattern) -> Iterator[int]:
    p = cycle(chain.from_iterable(repeat(i, index) for i in pattern))
    next(p)
    return p


def operate(prev_list: List[int], phase: Iterator[int]) -> int:
    result = reduce(add, (a * b for a, b in zip(prev_list, phase)))
    return int(str(result)[-1])


def fft(puzzle: str, n: int = 100) -> List[int]:
    prev_list = list(map(int, list(puzzle)))
    for _ in range(n):
        prev_list = [operate(prev_list, phase(i)) for i in range(1, len(prev_list) + 1)]
    return prev_list


if __name__ == "__main__":
    puzzle = Path("./day16_input.txt").read_text().strip()
    print(f"Solution for part 1: {''.join(str(i) for i in fft(puzzle)[:8])}")
