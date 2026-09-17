"""Estimate AUV propulsion and energy costs while navigating ocean currents."""


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

def ground_velocity_from_direction(
    direction: Vector,
    speed: float,
) -> Vector:
    """Scale a unit travel direction to the desired ground speed."""

    direction_x, direction_y = direction

    return direction_x * speed, direction_y * speed


def ground_velocity(
    current: Tuple[int, int],
    neighbour: Tuple[int, int],
    speed: float,
) -> Vector:
    """Calculate the desired ground velocity for one grid movement."""

    direction = travel_direction(current, neighbour)

    return ground_velocity_from_direction(direction, speed)
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
    travel_direction_vector: Vector | None = None,
    
) -> float:
    """Estimate propulsion energy required for one grid movement."""

    # Determine the AUV's desired velocity over the ground.
    if travel_direction_vector is None:
        desired_velocity = ground_velocity(
            current,
            neighbour,
            ground_speed,
        )
    else:
        desired_velocity = ground_velocity_from_direction(
            travel_direction_vector,
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

def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """Calculate the great-circle distance between two coordinates in meters."""

    earth_radius_m = 6_371_000

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

    return earth_radius_m * c

def geographic_travel_direction(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> Vector:
    """Return the physical east/north travel direction between nearby coordinates."""

    mean_lat = math.radians((lat1 + lat2) / 2)

    east = math.radians(lon2 - lon1) * math.cos(mean_lat)
    north = math.radians(lat2 - lat1)

    magnitude = math.sqrt(east**2 + north**2)

    return east / magnitude, north / magnitude