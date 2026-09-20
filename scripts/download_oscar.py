"""Download historical NASA OSCAR surface-current data for RNN training."""

from pathlib import Path

import earthaccess


OUTPUT_DIR = Path("data/raw/oscar_history")


def download_oscar_history():
    """Download OSCAR daily current fields for RNN training."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Authenticate using the NASA Earthdata credentials in ~/.netrc.
    earthaccess.login(strategy="netrc")

    # Find roughly two months of daily OSCAR current data.
    results = earthaccess.search_data(
        short_name="OSCAR_L4_OC_FINAL_V2.0",
        temporal=(
            "2025-07-15T00:00:00Z",
            "2025-09-15T23:59:59Z",
        ),
    )

    print(f"Found {len(results)} granule(s)")

    files = earthaccess.download(
        results,
        str(OUTPUT_DIR),
    )

    print(f"Downloaded {len(files)} file(s)")


if __name__ == "__main__":
    download_oscar_history()