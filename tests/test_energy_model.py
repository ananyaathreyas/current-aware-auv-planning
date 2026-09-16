"""Tests for AUV propulsion and energy calculations."""

import math

import pytest

from auv_planning.energy_model import (
    travel_direction,
    required_propulsion_velocity,
    vector_magnitude,
    movement_energy,
)


def test_diagonal_travel_direction():
    """A diagonal grid move should produce a normalized direction vector."""

    direction = travel_direction((0, 0), (1, 1))

    expected = 1 / math.sqrt(2)

    assert direction[0] == pytest.approx(expected)
    assert direction[1] == pytest.approx(expected)


def test_helping_current_reduces_propulsion():
    """A current moving with the AUV should reduce required propulsion."""

    propulsion = required_propulsion_velocity(
        ground_velocity=(1.0, 0.0),
        current_velocity=(0.4, 0.0),
    )

    assert propulsion == pytest.approx((0.6, 0.0))


def test_vector_magnitude():
    """Velocity magnitude should be calculated from both vector components."""

    magnitude = vector_magnitude((3.0, 4.0))

    assert magnitude == pytest.approx(5.0)


def test_current_direction_changes_energy_cost():
    """Helping currents should cost less energy than opposing currents."""

    helping = movement_energy(
        (0, 0),
        (1, 0),
        current_velocity=(0.4, 0.0),
        distance_m=500,
        ground_speed=1.0,
        power_coefficient=200,
    )

    neutral = movement_energy(
        (0, 0),
        (1, 0),
        current_velocity=(0.0, 0.0),
        distance_m=500,
        ground_speed=1.0,
        power_coefficient=200,
    )

    opposing = movement_energy(
        (0, 0),
        (1, 0),
        current_velocity=(-0.4, 0.0),
        distance_m=500,
        ground_speed=1.0,
        power_coefficient=200,
    )

    assert helping < neutral < opposing