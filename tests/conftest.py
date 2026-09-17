"""Shared pytest fixtures for constructing test ocean grids."""

import numpy as np
import pytest

from auv_planning.ocean_grid import OceanGrid


@pytest.fixture
def empty_grid():
    """Create a fully traversable 3x3 grid with no ocean currents."""

    latitudes = np.array([
        36.00,
        36.25,
        36.50,
    ])

    longitudes = np.array([
        -123.00,
        -122.75,
        -122.50,
    ])

    current_u = np.zeros((3, 3))
    current_v = np.zeros((3, 3))

    traversable = np.ones(
        (3, 3),
        dtype=bool,
    )

    return OceanGrid(
        latitudes=latitudes,
        longitudes=longitudes,
        current_u=current_u,
        current_v=current_v,
        traversable=traversable,
    )

@pytest.fixture
def obstacle_grid():
    """Create a grid with one blocked cell to test obstacle avoidance."""
    latitudes = np.array([
        36.00,
        36.25,
        36.50,
    ])

    longitudes = np.array([
        -123.00,
        -122.75,
        -122.50,
    ])

    current_u = np.zeros((3, 3))
    current_v = np.zeros((3, 3))

    traversable = np.ones((3, 3), dtype=bool)

    # Block center cell
    traversable[1, 1] = False

    return OceanGrid(
        latitudes=latitudes,
        longitudes=longitudes,
        current_u=current_u,
        current_v=current_v,
        traversable=traversable,
    )
@pytest.fixture
def blocked_grid():
    """Create a rectangular grid where a wall makes the goal unreachable."""

    latitudes = np.array([
        36.00,
        36.25,
        36.50,
    ])

    longitudes = np.array([
        -123.00,
        -122.75,
        -122.50,
        -122.25,
        -122.00,
    ])

    current_u = np.zeros((3, 5))
    current_v = np.zeros((3, 5))

    traversable = np.ones((3, 5), dtype=bool)

    # Block an entire column
    traversable[:, 2] = False

    return OceanGrid(
        latitudes=latitudes,
        longitudes=longitudes,
        current_u=current_u,
        current_v=current_v,
        traversable=traversable,
    )


@pytest.fixture
def irregular_grid():
    """Create a partially traversable 5x5 grid with irregular obstacles."""

    latitudes = np.array([
        36.00,
        36.25,
        36.50,
        36.75,
        37.00,
    ])

    longitudes = np.array([
        -123.00,
        -122.75,
        -122.50,
        -122.25,
        -122.00,
    ])

    current_u = np.zeros((5, 5))
    current_v = np.zeros((5, 5))

    # Mimic an irregular coastline or region of unavailable ocean cells.
    traversable = np.array([
        [True,  True,  True,  False, True],
        [True,  True,  False, False, True],
        [True,  True,  True,  False, True],
        [False, True,  True,  True,  True],
        [False, False, True,  True,  True],
    ])

    return OceanGrid(
        latitudes=latitudes,
        longitudes=longitudes,
        current_u=current_u,
        current_v=current_v,
        traversable=traversable,
    )

@pytest.fixture
def upward_current_field():
    """Create a grid where an upper route has a helpful eastward current."""

    latitudes = np.array([
        36.00,
        36.25,
        36.50,
    ])

    longitudes = np.array([
        -123.00,
        -122.75,
        -122.50,
        -122.25,
        -122.00,
    ])

    # u is east/west current velocity.
    # Give the top row a strong eastward current.
    current_u = np.array([
        [0.8, 0.8, 0.8, 0.8, 0.8],
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
    ])

    # No north/south current.
    current_v = np.zeros((3, 5))

    traversable = np.ones((3, 5), dtype=bool)

    return OceanGrid(
        latitudes=latitudes,
        longitudes=longitudes,
        current_u=current_u,
        current_v=current_v,
        traversable=traversable,
    )