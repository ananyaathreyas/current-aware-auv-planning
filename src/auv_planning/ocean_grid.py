from typing import Tuple, List
import numpy as np
class OceanGrid:
    def __init__(
            self,
            width:int,
            height:int,
            current_u:np.ndarray,
            current_v:np.ndarray,
            traversable:np.ndarray,
    ):
        self.width = width
        self.height = height
        self.current_u = current_u
        self.current_v = current_v
        self.traversable = traversable
    def get_neighbours(self, coordinates: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
            Get the neighboring coordinates of a given coordinate in a grid.
    
        Args:
            coordinates (Tuple[int, int]): The (x, y) coordinates of the current position.
    
        Returns:
            List[Tuple[int, int]]: A list of neighboring coordinates.
        """
        x, y = coordinates
        candidates = [
            (x + 1, y),     # Right
            (x - 1, y),     # Left
            (x, y + 1),     # Down
            (x, y - 1),     # Up
            (x + 1, y + 1), # Down-Right
            (x - 1, y - 1), # Up-Left
            (x + 1, y - 1), # Up-Right
            (x - 1, y + 1)  # Down-Left
        ]
        neighbors = []
    
        for candidate_x, candidate_y in candidates:
            if 0 <= candidate_x < self.width and 0 <= candidate_y < self.height:
                inside_grid = True
            else:
                inside_grid = False
    
            if not inside_grid or not self.traversable[candidate_y, candidate_x]:
                continue
            neighbors.append((candidate_x, candidate_y))
        return neighbors

    def get_current_at(self, coordinates: Tuple[int, int]) -> Tuple[float, float]:
        """
            Get the current vector (u, v) at a given coordinate in the grid.
    
        Args:
            coordinates (Tuple[int, int]): The (x, y) coordinates of the position.
    
        Returns:
            Tuple[float, float]: The current vector (u, v) at the given coordinates.
        """
        x, y = coordinates
        u = self.current_u[y, x]
        v = self.current_v[y, x]
        return u, v

    def get_location(self, coordinates: Tuple[int, int]) -> Tuple[float, float]:
        """
            Get the real-world location (latitude, longitude) corresponding to the grid coordinates.
    
        Args:
            coordinates (Tuple[int, int]): The (x, y) coordinates of the position in the grid.
    
        Returns:
            Tuple[float, float]: The real-world location (latitude, longitude) corresponding to the grid coordinates.
        """
        x, y = coordinates

        latitude = float(self.latitudes[y])
        longitude = float(self.longitudes[x])

        return latitude, longitude
