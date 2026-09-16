"""Tests for baseline A* path planning on synthetic ocean grids."""

from auv_planning.astar import astar


def test_astar_finds_path(empty_grid):
    """A* should find a path between two reachable cells."""
    path = astar(
        empty_grid,
        start=(0, 0),
        goal=(2, 2),
    )

    assert path is not None
    assert path[0] == (0, 0)
    assert path[-1] == (2, 2)

def test_astar_avoids_obstacle(obstacle_grid):
    """A* should route around obstacles without entering blocked cells."""
    path = astar(
        obstacle_grid,
        start=(0, 0),
        goal=(2, 2),
    )

    assert path is not None
    assert path[-1] == (2, 2)
    assert (1, 1) not in path
    for x, y in path:
        assert obstacle_grid.traversable[y, x]


def test_astar_returns_none_when_no_path(blocked_grid):
    """A* should return None when obstacles completely separate start and goal."""
    path = astar(
        blocked_grid,
        start=(0, 0),
        goal=(4, 2),
    )

    assert path is None

def test_astar_start_equals_goal(empty_grid):
    """A* should return a one-cell path when the start is already the goal."""
    path = astar(
        empty_grid,
        start=(1, 1),
        goal=(1, 1),
    )

    assert path == [(1, 1)]

def test_astar_uses_diagonal_path(empty_grid):
    """A* should use diagonal movement when it produces the shortest path."""
    path = astar(
        empty_grid,
        start=(0, 0),
        goal=(2, 2),
    )

    assert path == [
        (0, 0),
        (1, 1),
        (2, 2),
    ]

def test_astar_navigates_irregular_grid(irregular_grid):
    """A* should navigate an irregular region of blocked and traversable cells."""

    path = astar(
        irregular_grid,
        start=(0, 0),
        goal=(4, 4),
    )

    assert path is not None
    assert path[0] == (0, 0)
    assert path[-1] == (4, 4)

    for x, y in path:
        assert irregular_grid.traversable[y, x]