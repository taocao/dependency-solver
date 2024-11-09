from collections import defaultdict
from typing import Dict, List, Set


class DependencyError(Exception):
    """Custom exception for dependency-related errors."""

    pass


class ProjectScheduler:
    def __init__(self) -> None:
        self.graph: Dict[str, List[str]] = defaultdict(list)
        self.vertices: Set[str] = set()

    def add_dependency(self, task: str, dependency: str) -> None:
        """Add a dependency: task depends on dependency."""
        if not task or not dependency:
            raise DependencyError("Task and dependency must not be empty")
        self.graph[dependency].append(task)
        self.vertices.add(task)
        self.vertices.add(dependency)

    def validate_dependencies(self) -> None:
        """Validate the dependency graph for circular dependencies."""
        visited: Set[str] = set()
        temp: Set[str] = set()

        def dfs(vertex: str) -> None:
            if vertex in temp:
                raise DependencyError("Circular dependency detected")
            if vertex not in visited:
                temp.add(vertex)
                for adjacent in self.graph[vertex]:
                    dfs(adjacent)
                visited.add(vertex)
                temp.remove(vertex)

        for vertex in self.vertices:
            if vertex not in visited:
                dfs(vertex)

    def find_order(self) -> List[str]:
        """Find the optimal order of tasks."""
        self.validate_dependencies()
        visited: Set[str] = set()
        temp: Set[str] = set()
        stack: List[str] = []

        def dfs(vertex: str) -> None:
            if vertex not in visited:
                temp.add(vertex)
                for adjacent in self.graph[vertex]:
                    dfs(adjacent)
                visited.add(vertex)
                temp.remove(vertex)
                stack.append(vertex)

        for vertex in self.vertices:
            if vertex not in visited:
                dfs(vertex)

        return list(reversed(stack))
