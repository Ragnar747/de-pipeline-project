# Databricks notebook source
# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

import os
import sys

sys.path.append(os.path.abspath("../src"))

from olist_pipeline.config import BRONZE_SCHEMA, TABLE_KEYS
from olist_pipeline.profiling import profile_table

# COMMAND ----------

for table_name, keys in TABLE_KEYS.items():
    display(profile_table(spark, f"{BRONZE_SCHEMA}.{table_name}", keys))