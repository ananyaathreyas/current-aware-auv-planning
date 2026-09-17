"""Tests for current-aware A* path planning."""

import pytest

from auv_planning.astar import astar
from auv_planning.current_aware_astar import (
    current_aware_astar,
    edge_current,
    edge_distance,
)


def test_edge_current_averages_endpoints(empty_grid):
    """Edge current should average the current vectors at both endpoints."""

    empty_grid.current_u[0, 0] = 0.2
    empty_grid.current_v[0, 0] = 0.6

    empty_grid.current_u[0, 1] = 0.4
    empty_grid.current_v[0, 1] = 0.8

    current = edge_current(
        empty_grid,
        (0, 0),
        (1, 0),
    )

    assert current == pytest.approx((0.3, 0.7))


def test_edge_distance_uses_coordinates(empty_grid):
    """Edge distance should return a positive physical distance in meters."""

    distance = edge_distance(
        empty_grid,
        (0, 0),
        (1, 0),
    )
    assert distance > 0
def test_current_aware_astar_uses_helpful_current(upward_current_field):
    """Energy-aware planning should respond to a helpful eastward current."""

    start = (0, 1)
    goal = (4, 1)

    shortest_path = astar(
        upward_current_field,
        start=start,
        goal=goal,
    )

    energy_path = current_aware_astar(
        upward_current_field,
        start=start,
        goal=goal,
    )

    assert shortest_path is not None
    assert energy_path is not None

    assert shortest_path[0] == start
    assert shortest_path[-1] == goal

    assert energy_path[0] == start
    assert energy_path[-1] == goal

    # The distance-based planner should take the direct middle route.
    assert shortest_path == [
        (0, 1),
        (1, 1),
        (2, 1),
        (3, 1),
        (4, 1),
    ]

    # The energy-aware planner should detour through the helpful current.
    assert energy_path != shortest_path
    assert any(y == 0 for x, y in energy_path[1:-1])
