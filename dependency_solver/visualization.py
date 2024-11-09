from typing import Dict, List

import matplotlib.pyplot as plt
import networkx as nx


def create_dependency_graph(dependencies: Dict[str, List[str]]) -> nx.DiGraph:
    """Create a NetworkX directed graph from dependencies."""
    G = nx.DiGraph()

    for dependency, tasks in dependencies.items():
        for task in tasks:
            G.add_edge(dependency, task)

    return G


def visualize_graph(G: nx.DiGraph) -> plt.Figure:
    """Create a visualization of the dependency graph."""
    plt.clf()
    fig = plt.figure(figsize=(10, 8))

    pos = nx.spring_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=2000,
        arrowsize=20,
        font_size=14,
        font_weight="bold",
        edge_color="gray",
        width=2,
    )

    plt.title("Project Dependencies Graph", pad=20, size=16)
    return fig
