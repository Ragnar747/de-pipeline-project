"""Bronze layer: land raw source files as Delta tables, unchanged."""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, current_timestamp

from olist_pipeline.config import BRONZE_SCHEMA, RAW_VOLUME_PATH, SOURCE_TABLES


def ingest_file(spark: SparkSession, file_name: str, table_name: str) -> DataFrame:
    """Read one raw CSV and save it as a bronze Delta table."""
    path = f"{RAW_VOLUME_PATH}/{file_name}"
    df = (
        spark.read.option("header", True)
        .option("multiLine", True)
        .option("escape", '"')
        .csv(path)
    )
    df = (
        df.withColumn("_ingested_at", current_timestamp())
          .withColumn("_source_file", col("_metadata.file_path"))
    )
    table = f"{BRONZE_SCHEMA}.{table_name}"
    df.write.format("delta").mode("overwrite").saveAsTable(table)
    return df

def ingest_all(spark: SparkSession) -> None:
    """Ingest every source file listed in config into the bronze layer."""
    for file_name, table_name in SOURCE_TABLES.items():
        print(f"Ingesting {file_name} -> {BRONZE_SCHEMA}.{table_name}")
        ingest_file(spark, file_name, table_name)
    print("Bronze ingestion complete.")