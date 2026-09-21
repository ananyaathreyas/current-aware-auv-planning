"""Find minimum-energy AUV paths through ocean currents using A*."""

import heapq
from typing import Dict, List, Optional, Tuple
import math

from auv_planning.astar import reconstruct_path
from auv_planning.energy_model import (
    haversine_distance,
    movement_energy,
    geographic_travel_direction,
)
from auv_planning.ocean_grid import OceanGrid


Vector = Tuple[float, float]
Coordinate = Tuple[int, int]


def edge_current(
    grid: OceanGrid,
    current: Coordinate,
    neighbour: Coordinate,
) -> Vector:
    """Return the average ocean-current vector along an edge."""

    x1, y1 = current
    x2, y2 = neighbour

    u1 = grid.current_u[y1, x1]
    v1 = grid.current_v[y1, x1]

    u2 = grid.current_u[y2, x2]
    v2 = grid.current_v[y2, x2]

    average_u = (u1 + u2) / 2
    average_v = (v1 + v2) / 2

    return average_u, average_v

def maximum_current_speed(grid: OceanGrid) -> float:
    """Return the strongest valid ocean-current speed in the grid."""

    max_current_speed = 0.0

    for y in range(grid.current_u.shape[0]):
        for x in range(grid.current_u.shape[1]):
            if not grid.traversable[y, x]:
                continue

            u = grid.current_u[y, x]
            v = grid.current_v[y, x]

            current_speed = math.sqrt(u**2 + v**2)
            max_current_speed = max(max_current_speed, current_speed)

    return max_current_speed

def current_aware_astar(
    grid: OceanGrid,
    start: Coordinate,
    goal: Coordinate,
    ground_speed: float = 1.0,
    power_coefficient: float = 200.0,
) -> Optional[List[Coordinate]]:
    """Find a minimum-energy path through an OceanGrid."""

    max_current_speed = maximum_current_speed(grid)
    frontier = []
    heapq.heappush(frontier, (0.0, start))

    origin: Dict[Coordinate, Coordinate] = {}
    cost_so_far: Dict[Coordinate, float] = {
        start: 0.0
    }

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            return reconstruct_path(origin, current)

        for neighbour in grid.get_neighbours(current):

            # Average the ocean current across this movement.
            ocean_current = edge_current(
                grid,
                current,
                neighbour,
            )

            # Calculate the real physical distance between the cells.
            distance_m = edge_distance(
                grid,
                current,
                neighbour,
            )

            # Calculate the real east/north direction of travel.
            direction = edge_direction(
                grid,
                current,
                neighbour,
            )

            # Estimate how much propulsion energy this movement requires.
            edge_energy = movement_energy(
                current=current,
                neighbour=neighbour,
                current_velocity=ocean_current,
                distance_m=distance_m,
                ground_speed=ground_speed,
                power_coefficient=power_coefficient,
                travel_direction_vector=direction,
            )

            new_cost = cost_so_far[current] + edge_energy

            if (
                neighbour not in cost_so_far
                or new_cost < cost_so_far[neighbour]
            ):
                cost_so_far[neighbour] = new_cost
                origin[neighbour] = current

                remaining_energy = energy_heuristic(
                    grid,
                    neighbour,
                    goal,
                    ground_speed,
                    power_coefficient,
                    max_current_speed

                )

                priority = new_cost + remaining_energy

                heapq.heappush(
                    frontier,
                    (priority, neighbour),
                )

    return None

def edge_distance(
    grid: OceanGrid,
    current: Coordinate,
    neighbour: Coordinate,
) -> float:
    """Return the physical distance between neighboring grid cells in meters."""

    x1, y1 = current
    x2, y2 = neighbour

    lat1 = grid.latitudes[y1]
    lon1 = grid.longitudes[x1]

    lat2 = grid.latitudes[y2]
    lon2 = grid.longitudes[x2]

    return haversine_distance(
        lat1,
        lon1,
        lat2,
        lon2,
    )

def edge_direction(
    grid: OceanGrid,
    current: Coordinate,
    neighbour: Coordinate,
) -> Vector:
    """Return the physical east/north direction of travel between two cells."""

    x1, y1 = current
    x2, y2 = neighbour

    lat1 = grid.latitudes[y1]
    lon1 = grid.longitudes[x1]

    lat2 = grid.latitudes[y2]
    lon2 = grid.longitudes[x2]

    return geographic_travel_direction(
        lat1,
        lon1,
        lat2,
        lon2,
    )

def energy_heuristic(
    grid: OceanGrid,
    current: Coordinate,
    goal: Coordinate,
    ground_speed: float,
    power_coefficient: float,
    max_current_speed: float,
) -> float:
    """Return an optimistic lower bound on energy needed to reach the goal."""

    x1, y1 = current
    x2, y2 = goal

    # Straight-line physical distance to the goal.
    remaining_distance = haversine_distance(
        grid.latitudes[y1],
        grid.longitudes[x1],
        grid.latitudes[y2],
        grid.longitudes[x2],
    )

    # Best case: the strongest current helps perfectly for the whole trip.
    minimum_propulsion_speed = max(
        0.0,
        ground_speed - max_current_speed,
    )

    minimum_power = (
        power_coefficient
        * minimum_propulsion_speed**3
    )

    minimum_travel_time = (
        remaining_distance / ground_speed
    )

    return minimum_power * minimum_travel_time