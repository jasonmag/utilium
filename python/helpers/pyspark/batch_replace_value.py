#!/usr/bin/env python3
"""
Usage:
    python batch_replace_value.py \
        --input /home/jason/data/input \
        --output /home/jason/data/output \
        --column EXTRACT_DATE_TIME \
        --from_value 2.02406E+13 \
        --to_value 20240601
"""

import os
import shutil
import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit

# --- Parse arguments ---
parser = argparse.ArgumentParser(description="Replace specific value in a given column across CSV files")
parser.add_argument("--input", required=True, help="Input directory with CSV files")
parser.add_argument("--output", required=True, help="Output directory for processed CSV files")
parser.add_argument("--column", required=True, help="Column name to perform the replacement")
parser.add_argument("--from_value", required=True, help="Value to search for (e.g. 2.02406E+13)")
parser.add_argument("--to_value", required=True, help="Value to replace with (e.g. 20240601)")
args = parser.parse_args()

input_dir = args.input
output_dir = args.output
column = args.column
from_value = args.from_value
to_value = args.to_value
temp_dir = os.path.join(output_dir, "_temp")

# Try to parse from_value as float (e.g., for scientific notation)
try:
    from_value_casted = float(from_value)
except ValueError:
    from_value_casted = from_value  # leave as string

# --- Spark session ---
spark = SparkSession.builder \
    .appName("Column Value Replacer") \
    .master("local[*]") \
    .getOrCreate()

os.makedirs(output_dir, exist_ok=True)

# --- Process each file ---
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        input_path = os.path.join(input_dir, filename)
        print(f"🔄 Processing {filename}...")

        df = spark.read.option("header", True).csv(input_path)

        if column not in df.columns:
            print(f"⚠️ Column '{column}' not found in {filename}, skipping.")
            continue

        # Cast to double if applicable
        df_replaced = df.withColumn(
            column,
            when(
                col(column).cast("double") == from_value_casted,
                lit(to_value)
            ).otherwise(col(column))
        )

        df_replaced.coalesce(1).write.option("header", True).mode("overwrite").csv(temp_dir)

        # Move part file to final output
        part_file = next((f for f in os.listdir(temp_dir) if f.startswith("part-")), None)
        if part_file:
            shutil.move(
                os.path.join(temp_dir, part_file),
                os.path.join(output_dir, filename)
            )
            shutil.rmtree(temp_dir)
        else:
            print(f"❌ Failed to write output for {filename}")

        print(f"✅ Saved updated file: {os.path.join(output_dir, filename)}")

spark.stop()

