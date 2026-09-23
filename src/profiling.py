"""Quick data profiling for any table."""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def profile_table(spark: SparkSession, table: str, keys: list[str]) -> DataFrame:
    """Print row and duplicate counts; return null counts for every column."""
    df = spark.table(table)
    total = df.count()
    unique_keys = df.select(*keys).distinct().count()
    print(f"{table}: {total} rows | {unique_keys} unique {keys} | {total - unique_keys} duplicates")

    null_counts = df.select(
        [F.count(F.when(F.col(c).isNull(), 1)).alias(c) for c in df.columns]
    ).collect()[0].asDict()

    rows = [(c, n, round(100 * n / total, 2)) for c, n in null_counts.items()]
    return spark.createDataFrame(rows, ["column", "null_count", "null_pct"])