import matplotlib.pyplot as plt
import networkx as nx

from dependency_solver.visualization import (create_dependency_graph,
                                             visualize_graph)


def test_create_dependency_graph():
    dependencies = {"a": ["b", "c"], "b": ["d"]}
    G = create_dependency_graph(dependencies)
    assert isinstance(G, nx.DiGraph)
    assert list(G.edges()) == [("a", "b"), ("a", "c"), ("b", "d")]


def test_visualize_graph():
    G = nx.DiGraph()
    G.add_edge("a", "b")
    fig = visualize_graph(G)
    assert isinstance(fig, plt.Figure)
