from unittest.mock import MagicMock, patch

import pytest

from dependency_solver.core import DependencyError
from dependency_solver.ui import DependencyUI


@pytest.fixture
def ui():
    return DependencyUI()


@pytest.fixture
def mock_streamlit():
    with patch("dependency_solver.ui.st") as mock_st:
        yield mock_st


def test_scheduler_initialization(ui):
    assert ui.scheduler is not None
    assert hasattr(ui.scheduler, "graph")
    assert hasattr(ui.scheduler, "vertices")


def test_reset_scheduler(ui):
    # Add some dependencies
    ui.scheduler.add_dependency("b", "a")
    ui.scheduler.add_dependency("c", "b")

    # Reset
    ui.reset_scheduler()

    # Check if scheduler is empty
    assert len(ui.scheduler.graph) == 0
    assert len(ui.scheduler.vertices) == 0


@pytest.mark.asyncio
async def test_render_input_form(mock_streamlit, ui):
    # Mock form inputs
    mock_streamlit.form.return_value.__enter__ = MagicMock()
    mock_streamlit.form.return_value.__exit__ = MagicMock()
    mock_streamlit.text_input.side_effect = ["task1", "dep1"]
    mock_streamlit.form_submit_button.return_value = True

    # Test form rendering
    task, dependency, submitted = ui.render_input_form()

    assert task == "task1"
    assert dependency == "dep1"
    assert submitted is True


def test_solve_dependencies_success(ui):
    # Add valid dependencies
    ui.scheduler.add_dependency("b", "a")
    ui.scheduler.add_dependency("c", "b")

    with patch("dependency_solver.ui.st") as mock_st:
        order = ui.solve_dependencies()

    assert order is not None
    assert len(order) == 3
    assert order.index("a") < order.index("b")
    assert order.index("b") < order.index("c")


def test_solve_dependencies_circular(ui):
    # Add circular dependencies
    ui.scheduler.add_dependency("b", "a")
    ui.scheduler.add_dependency("a", "b")

    with patch("dependency_solver.ui.st") as mock_st:
        order = ui.solve_dependencies()

    assert order is None
    mock_st.error.assert_called_once()


@pytest.mark.asyncio
async def test_render_visualization(mock_streamlit, ui):
    # Add some dependencies
    ui.scheduler.add_dependency("b", "a")
    ui.scheduler.add_dependency("c", "b")

    # Test visualization rendering
    ui.render_visualization()

    # Verify that subheader was called
    mock_streamlit.subheader.assert_called_with("Dependency Graph")

    # Verify that pyplot was called (indicating graph was rendered)
    mock_streamlit.pyplot.assert_called_once()


def test_render_current_dependencies(mock_streamlit, ui):
    # Add some dependencies
    ui.scheduler.add_dependency("b", "a")
    ui.scheduler.add_dependency("c", "b")

    # Test dependencies table rendering
    ui.render_current_dependencies()

    # Verify that subheader was called
    mock_streamlit.subheader.assert_called_with("Current Dependencies")

    # Verify that dataframe was displayed
    mock_streamlit.dataframe.assert_called_once()


@pytest.mark.asyncio
async def test_full_ui_workflow(mock_streamlit, ui):
    # Mock form submission
    mock_streamlit.form.return_value.__enter__ = MagicMock()
    mock_streamlit.form.return_value.__exit__ = MagicMock()
    mock_streamlit.text_input.side_effect = ["b", "a"]
    mock_streamlit.form_submit_button.return_value = True

    # Test complete workflow
    ui.render()

    # Verify page configuration
    mock_streamlit.set_page_config.assert_called_once()

    # Verify title was set
    mock_streamlit.title.assert_called_once()

    # Verify columns were created
    mock_streamlit.columns.assert_called_once_with([1, 2])


def test_error_handling(mock_streamlit, ui):
    # Test adding invalid dependency
    with pytest.raises(DependencyError):
        ui.scheduler.add_dependency("", "")

    # Verify error message
    mock_streamlit.error.assert_not_called()


if __name__ == "__main__":
    pytest.main(["-v", "test_ui.py"])
