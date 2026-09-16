"""Estimate AUV propulsion and energy costs in ocean currents.
    while AUV maintains the same speed through water.
"""


import math
from typing import Tuple


Vector = Tuple[float, float]


def travel_direction(
    current: Tuple[int, int],
    neighbour: Tuple[int, int],
) -> Vector:
    """Return a (normalized) unit vector pointing from the current cell to the next cell."""

    dx = neighbour[0] - current[0]
    dy = neighbour[1] - current[1]

    distance = math.sqrt(dx**2 + dy**2)

    return dx / distance, dy / distance

def ground_velocity(
    current: Tuple[int, int],
    neighbour: Tuple[int, int],
    speed: float,
) -> Vector:
    """Calculate the desired ground velocity for one grid movement."""

    direction_x, direction_y = travel_direction(current, neighbour)

    return direction_x * speed, direction_y * speed

def required_propulsion_velocity(
    ground_velocity: Vector,
    current_velocity: Vector,
) -> Vector:
    """Calculate the propulsion velocity needed to maintain the ground velocity."""

    ground_u, ground_v = ground_velocity
    current_u, current_v = current_velocity

    return (
        ground_u - current_u,
        ground_v - current_v,
    )

def vector_magnitude(vector: Vector) -> float:
    """Return the magnitude of a 2D velocity vector."""

    u, v = vector
    return math.sqrt(u**2 + v**2)

def propulsion_power(
    propulsion_speed: float,
    power_coefficient: float,
) -> float:
    """Estimate propulsion power from the AUV's speed through the water."""

    return power_coefficient * propulsion_speed**3
def energy_consumed(
    power: float,
    travel_time: float,
) -> float:
    """Calculate energy consumed over a period of time in joules."""

    return power * travel_time

def movement_energy(
    current: Tuple[int, int],
    neighbour: Tuple[int, int],
    current_velocity: Vector,
    distance_m: float,
    ground_speed: float,
    power_coefficient: float,
) -> float:
    """Estimate propulsion energy required for one grid movement."""

    # Determine the AUV's desired velocity over the ground.
    desired_velocity = ground_velocity(
        current,
        neighbour,
        ground_speed,
    )

    # Determine how much velocity the motors must provide after accounting
    # for the ocean current.
    propulsion_velocity = required_propulsion_velocity(
        desired_velocity,
        current_velocity,
    )

    propulsion_speed = vector_magnitude(propulsion_velocity)

    # Estimate the propulsion power required at that speed.
    power = propulsion_power(
        propulsion_speed,
        power_coefficient,
    )

    # Time depends on physical distance and desired ground speed.
    travel_time = distance_m / ground_speed

    # Energy = power × time, giving Joules.
    return energy_consumed(power, travel_time)