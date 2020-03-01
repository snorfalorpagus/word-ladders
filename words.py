import sys
import re
from functools import partial
from typing import Iterator, List
import networkx as nx
from networkx.drawing.nx_pydot import write_dot


def load_wordlist(filename: str) -> Iterator[str]:
    with open(filename, "r") as f:
        words = (line.strip().lower() for line in f.readlines())
    return words


def filter_words(words: Iterator[str]) -> List[str]:
    """Filter only 4 letter words"""
    pattern = re.compile("^[a-z]{4,4}$")
    match = partial(pattern.match)
    return list(filter(match, words))


def difference(word1: str, word2: str) -> int:
    """Returns the number of letters different between two words"""
    count = sum((
        1 if letter1 != letter2 else 0
        for letter1, letter2 in zip(word1, word2)
    ))
    return count


def build_graph(words: List[str]) -> nx.Graph:
    G = nx.Graph()
    for word1 in words:
        for word2 in words:
            if difference(word1, word2) == 1:
                G.add_edge(word1, word2)
    return G


def paths_to_digraph(paths: List[List[str]]) -> nx.DiGraph:
    """Transform a list of paths to a directional graph"""
    g = nx.DiGraph()
    for path in paths:
        for source, target in zip(path[:-1], path[1:]):
            g.add_edge(source, target)
    return g


def main():
    words = load_wordlist("words.txt")
    words = filter_words(words)
    G = build_graph(words)
    paths = nx.all_shortest_paths(G, "arty", "elks")
    g = paths_to_digraph(paths)
    write_dot(g, "paths.dot")


if __name__ == "__main__":
    sys.exit(main())
