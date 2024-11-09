from typing import List, Optional, Tuple

import pandas as pd
import streamlit as st

from dependency_solver.core import DependencyError, ProjectScheduler
from dependency_solver.visualization import (create_dependency_graph,
                                             visualize_graph)


class DependencyUI:
    def __init__(self):
        self.scheduler: ProjectScheduler = self._get_scheduler()

    @staticmethod
    def _get_scheduler() -> ProjectScheduler:
        """Get or create scheduler from session state."""
        if "scheduler" not in st.session_state:
            st.session_state.scheduler = ProjectScheduler()
        return st.session_state.scheduler

    def reset_scheduler(self) -> None:
        """Reset the scheduler state."""
        st.session_state.scheduler = ProjectScheduler()
        self.scheduler = st.session_state.scheduler

    def render_input_form(self) -> Tuple[str, str, bool]:
        """Render the input form for dependencies."""
        with st.form(key="dependency_form"):
            task = st.text_input("Task", key="task_input")
            dependency = st.text_input("Depends on", key="dependency_input")
            submit_button = st.form_submit_button(label="Add Dependency")
            return task, dependency, submit_button

    def render_current_dependencies(self) -> None:
        """Display current dependencies in a table."""
        st.subheader("Current Dependencies")
        dependencies_list = []
        for dep in self.scheduler.graph:
            for task in self.scheduler.graph[dep]:
                dependencies_list.append({"Task": task, "Depends On": dep})

        if dependencies_list:
            df = pd.DataFrame(dependencies_list)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No dependencies added yet")

    def solve_dependencies(self) -> Optional[List[str]]:
        """Solve and display the dependency order."""
        try:
            order = self.scheduler.find_order()
            st.success("Optimal order: " + " → ".join(order))
            return order
        except DependencyError as e:
            st.error(str(e))
            return None

    def render_visualization(self) -> None:
        """Render the dependency graph visualization."""
        st.subheader("Dependency Graph")
        if self.scheduler.vertices:
            try:
                G = create_dependency_graph(self.scheduler.graph)
                fig = visualize_graph(G)
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Error generating visualization: {str(e)}")
        else:
            st.info("Add some dependencies to see the graph visualization")

    def render_example(self) -> None:
        """Render example section."""
        with st.expander("See Example"):
            st.write(
                """
            Example dependencies:
            - Task 'd' depends on 'a'
            - Task 'b' depends on 'f'
            - Task 'c' depends on 'a'
            - Task 'e' depends on 'b'
            - Task 'e' depends on 'c'
            """
            )

    def render(self) -> None:
        """Render the complete UI."""
        st.set_page_config(page_title="Project Dependency Solver", layout="wide")
        st.title("🏭 Project Dependency Solver")
        st.write(
            """
        This tool helps you determine the optimal order of tasks based on their dependencies.
        Add your tasks and their dependencies below, and the system will calculate the best sequence.
        """
        )

        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Add Dependencies")
            task, dependency, submit_button = self.render_input_form()

            if submit_button and task and dependency:
                try:
                    self.scheduler.add_dependency(task, dependency)
                    st.success(f"Added: {task} depends on {dependency}")
                except DependencyError as e:
                    st.error(str(e))

            if st.button("Reset All"):
                self.reset_scheduler()
                st.success("All dependencies cleared!")

            self.render_current_dependencies()

            if st.button("Solve Dependencies"):
                self.solve_dependencies()

        with col2:
            self.render_visualization()
            self.render_example()


def main() -> None:
    """Main entry point for the Streamlit application."""
    ui = DependencyUI()
    ui.render()


if __name__ == "__main__":
    main()
