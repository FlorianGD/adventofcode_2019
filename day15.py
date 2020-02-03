"""AoC 2019 day 15: Oxygen System"""

from intcode import Program, read_input
from collections import defaultdict
from typing import Dict, DefaultDict, List, Tuple, Union, Set

Grid = Dict[complex, int]

moves: Dict[int, complex] = {1: 1j, 2: -1j, 3: 1, 4: -1}
# moves to backtrack
back: Dict[int, int] = {1: 2, 2: 1, 3: 4, 4: 3}


def explore(program: Program) -> Grid:
    program.reset()
    available_moves: DefaultDict[complex, List[int]] = defaultdict(lambda: [4, 2, 3, 1])
    backtracking: List[int] = list()
    grid: Grid = dict()
    position = 0j
    available_moves[position]  # init to enter the loop
    while any(available_moves.values()) or backtracking:
        if available_moves[position]:
            direction = available_moves[position].pop()
            program.add_input(direction)
            status = next(program.operate())
            grid[position + moves[direction]] = status
            if status in [1, 2]:
                backtracking.append(back[direction])
                position += moves[direction]
            else:
                # We hit a wall, don't move
                continue
        else:
            # no move available, backtrack
            direction = backtracking.pop()
            program.add_input(direction)
            next(program.operate())  # we know it will be 1
            position += moves[direction]
    return grid


Node = Union[None, complex]


def dijsktra(grid: Grid, initial: Node = 0j) -> List[complex]:
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths: Dict[Node, Tuple[Node, int]] = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node is not None and grid[current_node] != 2:
        visited.add(current_node)
        destinations = [
            current_node + a for a in (1, -1, 1j, -1j) if grid[current_node + a] != 0
        ]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = weight_to_current_node + 1
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {
            node: shortest_paths[node] for node in shortest_paths if node not in visited
        }
        if not next_destinations:
            raise ValueError("Route Not Possible")
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path: List[complex] = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path


def print_grid(grid: Grid) -> None:
    min_i = int(min(map(lambda x: x.real, grid.keys())))
    max_i = int(max(map(lambda x: x.real, grid.keys())))
    min_j = int(min(map(lambda x: x.imag, grid.keys())))
    max_j = int(max(map(lambda x: x.imag, grid.keys())))
    element = {0: "#", 1: " ", 2: "@", 3: "?"}
    # header
    print("".join(" " if i >= 0 else "-" for i in range(min_i, max_i + 1)))
    print("".join(str(abs(i) // 10) for i in range(min_i, max_i + 1)))
    print("".join(str(abs(i) % 10) for i in range(min_i, max_i + 1)))
    print()
    # grid + line number
    for j in range(max_j, min_j - 1, -1):
        for i in range(min_i, max_i + 1):
            print(element[grid.get(i + j * 1j, 3)], end="")
        print(" ", j)


# part 2


def fill_grid(
    grid: Grid, start: complex, time: int = 0, visited: Set[complex] = set()
) -> int:
    visited.add(start)
    next_avail = {start + a for a in (1, 1j, -1, -1j) if grid[start + a] != 0} - visited
    if not next_avail:
        return time
    else:
        return max(fill_grid(grid, n, time + 1, visited) for n in next_avail)


if __name__ == "__main__":
    program = Program(read_input("./day15_input.txt"))
    grid = explore(program)
    print_grid(grid)
    print(f"Solution for part 1: {len(dijsktra(grid) )- 1}")
    target = next(a for a, b in grid.items() if b == 2)
    # visited = set()
    print(f"Solution for part 2: {fill_grid(grid, target)}")
