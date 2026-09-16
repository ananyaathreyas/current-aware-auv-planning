"""Find minimum-energy AUV paths through ocean currents using A*."""

import heapq
from typing import Dict, List, Optional, Tuple

from auv_planning.astar import reconstruct_path
from auv_planning.energy_model import (
    haversine_distance,
    movement_energy,
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

def current_aware_astar(
    grid: OceanGrid,
    start: Coordinate,
    goal: Coordinate,
    ground_speed: float = 1.0,
    power_coefficient: float = 200.0,
) -> Optional[List[Coordinate]]:
    """Find a minimum-energy path through an OceanGrid."""

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

            ocean_current = edge_current(
                grid,
                current,
                neighbour,
            )
            distance_m = edge_distance(
                grid,
                current,
                neighbour,
)

            edge_energy = movement_energy(
                current=current,
                neighbour=neighbour,
                current_velocity=ocean_current,
                distance_m=distance_m,
                ground_speed=ground_speed,
                power_coefficient=power_coefficient,
            )

            new_cost = cost_so_far[current] + edge_energy

            if (
                neighbour not in cost_so_far
                or new_cost < cost_so_far[neighbour]
            ):
                cost_so_far[neighbour] = new_cost
                origin[neighbour] = current

                heapq.heappush(
                    frontier,
                    (new_cost, neighbour),
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