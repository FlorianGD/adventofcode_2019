"""Aoc 2019 day 6: Universal Orbit Map"""
import networkx as nx
from typing import List, Tuple
from pathlib import Path
from networkx.algorithms.dag import ancestors
from networkx.algorithms.shortest_paths.generic import shortest_path

def puzzle_to_graph() -> nx.DiGraph:
    puzzle = Path("./day06_input.txt").read_text().splitlines()
    edges = [tuple(l.split(")")) for l in puzzle]
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G


def length_of_each_nodes(graph: nx.DiGraph) -> int:
    return sum(len(ancestors(G, node)) for node in G.nodes)


G = puzzle_to_graph()
print(f"Solution for part 1: {length_of_each_nodes(G)}")

# We are required to find the shortest path between YOU and SAN. The networkx function
# returns a list of nodes, including YOU and SAN, so we have to count them out. We
# further need to withdraw one because we want to go one step before SAN, not to SAN
# exactly. This explains the "-3" below.
print(f"Solution for part 2: {len(shortest_path(nx.Graph(G), 'YOU', 'SAN')) - 3}")