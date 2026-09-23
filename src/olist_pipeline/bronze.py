"""Bronze layer: land raw source files as delta tables, unchaged"""

from pyspark.sql import DataFrame, SparkSession
form pyspark.sql.functions import col, current_timestamp

from olist_pipeline.config import RAW_VOLUME_PATH, BRONZE_SCHEMA, SOURCE_TABLES

def ingest_file(spark: SparkSession, file_name: str, table_naem: str) -> DataFrame:
    """Read one raw CSV and save it as bronze Delta table """
    path = f"{RAW_VOLUME_PATH}/{file_name}"
    df = spark.read.option('header', TRUE).csv(path)

df = (
    df.withColumn("ingested_at", current_timestamp())
      .withColumn("source_file", col('metadata.file_path'))
)

table = f"{BRONZE_SCHEMA}.{table_name}"
df.write.format("delta").mode("overwrite").saveAsTable(table)
return df


def ingest_all_files(spark: SparkSession) -> None:
    """ Ingest every source file listed in config into the bronze layer"""
    for file_name, table_name in SOURCE_TABLES.items():
        print(f'Ingesting {file_name} -> {BRONZE_SCHEMA}.{table_name}')
        ingest_file(spark, file_name, table_name)
    print("Bronze ingestion complete.")
    