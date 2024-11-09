import pytest

from dependency_solver.core import DependencyError, ProjectScheduler


def test_add_dependency():
    scheduler = ProjectScheduler()
    scheduler.add_dependency("b", "a")
    assert "a" in scheduler.graph
    assert "b" in scheduler.graph["a"]
    assert {"a", "b"} == scheduler.vertices


def test_empty_dependency():
    scheduler = ProjectScheduler()
    with pytest.raises(DependencyError):
        scheduler.add_dependency("", "a")
    with pytest.raises(DependencyError):
        scheduler.add_dependency("a", "")


def test_circular_dependency():
    scheduler = ProjectScheduler()
    scheduler.add_dependency("b", "a")
    scheduler.add_dependency("c", "b")
    scheduler.add_dependency("a", "c")

    with pytest.raises(DependencyError, match="Circular dependency detected"):
        scheduler.validate_dependencies()


def test_find_order():
    scheduler = ProjectScheduler()
    scheduler.add_dependency("b", "a")
    scheduler.add_dependency("c", "b")

    order = scheduler.find_order()
    assert order.index("a") < order.index("b")
    assert order.index("b") < order.index("c")
