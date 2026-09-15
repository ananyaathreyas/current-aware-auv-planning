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
