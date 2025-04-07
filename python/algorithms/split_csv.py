#!/usr/bin/env python3
"""
split_csv.py

A utility script to split a CSV file into multiple smaller CSV files.

Features:
- Supports CSV files with or without headers
- Split by specifying number of output files OR number of rows per file
- Defaults to 100 rows per file if no option is specified
- Output files retain the original filename with _part_X suffix

Usage:
    python split_csv.py data.csv --header
    python split_csv.py data.csv --header --num-files 5
    python split_csv.py data.csv --rows 50

Author: jasonmag
"""

import csv
import os
import argparse
from math import ceil

def split_csv(input_file, has_header=True, num_files=None, rows_per_file=100):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    ext = os.path.splitext(input_file)[1] or ".csv"

    with open(input_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    header = rows[0] if has_header else []
    data = rows[1:] if has_header else rows

    if num_files:
        rows_per_file = ceil(len(data) / num_files)

    total_parts = ceil(len(data) / rows_per_file)

    for i in range(total_parts):
        start = i * rows_per_file
        end = start + rows_per_file
        chunk = data[start:end]
        output_filename = f"{base_name}_part_{i + 1}{ext}"
        with open(output_filename, "w", newline='', encoding='utf-8') as out_file:
            writer = csv.writer(out_file)
            if has_header:
                writer.writerow(header)
            writer.writerows(chunk)
        print(f"✅ Created {output_filename} with {len(chunk)} rows")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a CSV file into smaller files by row count or number of files.")
    parser.add_argument("file", help="Path to the CSV file")
    parser.add_argument("--header", action="store_true", help="Specify if the CSV file has a header")
    parser.add_argument("--num-files", type=int, help="Number of files to split into")
    parser.add_argument("--rows", type=int, default=100, help="Number of rows per file (default: 100)")

    args = parser.parse_args()
    split_csv(
        input_file=args.file,
        has_header=args.header,
        num_files=args.num_files,
        rows_per_file=args.rows
    )

