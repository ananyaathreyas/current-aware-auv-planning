import heapq
import math
from typing import Dict, List, Optional, Tuple

from auv_planning.ocean_grid import OceanGrid


Coordinate = Tuple[int, int]


def heuristic(a: Coordinate, b: Coordinate) -> float:
    """Estimate remaining distance using Euclidean distance."""

    dx = b[0] - a[0]
    dy = b[1] - a[1]

    return math.sqrt(dx**2 + dy**2)

def movement_distance(a: Coordinate, b: Coordinate) -> float:
    """Return grid distance between neighboring cells."""

    dx = b[0] - a[0]
    dy = b[1] - a[1]

    return math.sqrt(dx**2 + dy**2)
def reconstruct_path(origin: Dict[Coordinate, Coordinate], current:Coordinate) -> List[Coordinate]:
    """Reconstruct the path from the origin dictionary."""

    total_path = [current]

    while current in origin:
        current = origin[current]
        total_path.append(current)

    return total_path[::-1]  
def astar(
    grid: OceanGrid,
    start: Coordinate,
    goal: Coordinate,
) -> Optional[List[Coordinate]]:
    """Find the shortest path through an OceanGrid using A*."""

    frontier = []

    heapq.heappush(
        frontier,
        (0.0, start),
    )

    origin: Dict[Coordinate, Coordinate] = {}

    cost_so_far: Dict[Coordinate, float] = {
        start: 0.0
    }

    while frontier:
        priority, current = heapq.heappop(frontier)

        if current == goal:
            return reconstruct_path(origin, current)

        for neighbour in grid.get_neighbours(current):

            new_cost = (
                cost_so_far[current]
                + movement_distance(current, neighbour)
            )

            if (
                neighbour not in cost_so_far
                or new_cost < cost_so_far[neighbour]
            ):
                cost_so_far[neighbour] = new_cost

                priority = (
                    new_cost
                    + heuristic(neighbour, goal)
                )

                heapq.heappush(
                    frontier,
                    (priority, neighbour),
                )

                origin[neighbour] = current

    return None