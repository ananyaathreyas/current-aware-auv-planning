"""Tests for current-aware A* path planning."""

import pytest

from auv_planning.current_aware_astar import (
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

