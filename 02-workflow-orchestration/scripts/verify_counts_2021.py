#!/usr/bin/env python3
"""Download green/yellow taxi files for 2021 months (01..07) and count rows.
This script is meant for quick local verification before/after running flows.
"""
import gzip
import io
import sys
from urllib.request import urlopen

PREFIX_YELLOW = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
PREFIX_GREEN = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/"

months = [f"{i:02d}" for i in range(1, 8)]


def count_rows_from_gz(url):
    with urlopen(url) as resp:
        data = resp.read()
    # Use gzip module to decompress to avoid writing to disk
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as f:
        lines = f.read().splitlines()
    # subtract 1 for header
    return max(0, len(lines) - 1), len(data)


if __name__ == "__main__":
    for taxi, prefix in ("yellow", PREFIX_YELLOW), ("green", PREFIX_GREEN):
        total_rows = 0
        print(f"\n{taxi.upper()} 2021 (months 01..07):")
        for m in months:
            url = f"{prefix}{taxi}_tripdata_2021-{m}.csv.gz"
            try:
                rows, compressed_bytes = count_rows_from_gz(url)
                total_rows += rows
                print(f"  {m}: rows={rows:,} compressed_size={compressed_bytes/1024/1024:.2f} MiB")
            except Exception as e:
                print(f"  {m}: ERROR fetching {url}: {e}")
        print(f"TOTAL rows (data lines) for {taxi} 2021 months 01..07: {total_rows:,}\n")

# Example: python scripts/verify_counts_2021.py
