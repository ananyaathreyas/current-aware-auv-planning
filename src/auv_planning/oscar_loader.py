"""Load NASA OSCAR surface-current data into an OceanGrid."""

from pathlib import Path

import numpy as np
import xarray as xr

from auv_planning.ocean_grid import OceanGrid


def load_oscar_region(
    filepath: str | Path,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
) -> OceanGrid:
    """Load a geographic subset of an OSCAR NetCDF file."""

    ds = xr.open_dataset(filepath)

    # OSCAR stores longitude from 0 to 360 degrees.
    west = min_lon % 360
    east = max_lon % 360

    # Select only the geographic region we want.
    region = ds.where(
        (ds.lat >= min_lat)
        & (ds.lat <= max_lat)
        & (ds.lon >= west)
        & (ds.lon <= east),
        drop=True,
    )

    # OSCAR stores arrays as [longitude, latitude].
    # OceanGrid expects [latitude, longitude] == [y, x].
    current_u = (
        region.u
        .isel(time=0)
        .transpose("latitude", "longitude")
        .values
    )

    current_v = (
        region.v
        .isel(time=0)
        .transpose("latitude", "longitude")
        .values
    )

    latitudes = region.lat.values

    # Convert OSCAR longitudes from 0–360 to -180–180.
    longitudes = ((region.lon.values + 180) % 360) - 180

    # Missing current measurements cannot be used by the planner.
    traversable = np.isfinite(current_u) & np.isfinite(current_v)

    return OceanGrid(
        current_u=current_u,
        current_v=current_v,
        traversable=traversable,
        latitudes=latitudes,
        longitudes=longitudes,
    )