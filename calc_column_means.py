#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate mean value for each column.")
    parser.add_argument("file", help="Input file path (TSV/CSV).")
    parser.add_argument(
        "--delimiter",
        default="\t",
        help="Column delimiter. Default is tab (TSV).",
    )
    return parser.parse_args()


def to_float(value: str):
    value = value.strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def main() -> None:
    args = parse_args()
    file_path = Path(args.file)
    if not file_path.exists():
        raise SystemExit(f"File not found: {file_path}")

    with file_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter=args.delimiter)
        rows = list(reader)

    if not rows:
        raise SystemExit("Input file is empty.")

    max_cols = max(len(row) for row in rows)
    sums = [0.0] * max_cols
    counts = [0] * max_cols

    for row in rows:
        for i in range(max_cols):
            if i >= len(row):
                continue
            num = to_float(row[i])
            if num is None:
                continue
            sums[i] += num
            counts[i] += 1

    print(f"File: {file_path}")
    for i in range(max_cols):
        if counts[i] == 0:
            print(f"Column {i + 1}: no numeric values")
            continue
        mean = sums[i] / counts[i]
        print(f"Column {i + 1}: mean={mean:.6f}, count={counts[i]}")


if __name__ == "__main__":
    main()