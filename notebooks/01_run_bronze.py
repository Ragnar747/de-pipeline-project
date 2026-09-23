# Databricks notebook source
import os
import sys

sys.path.append(os.path.abspath("../src"))

from olist_pipeline.bronze import ingest_all
from olist_pipeline.config import BRONZE_SCHEMA

# COMMAND ----------

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {BRONZE_SCHEMA}")
ingest_all(spark)
