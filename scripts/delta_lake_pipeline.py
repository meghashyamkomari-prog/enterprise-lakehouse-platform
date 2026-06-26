from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, lit
from delta import configure_spark_with_delta_pip
import pandas as pd
from datetime import datetime

# Configure Spark with Delta Lake
builder = SparkSession.builder \
    .appName("EnterpriseLakehouse") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

print("✅ Spark Session with Delta Lake initialized!")

# Generate sample financial data
data = [
    ("AAPL", 150.25, 152.80, 149.10, 151.50, 1000000, "2026-06-25"),
    ("MSFT", 380.00, 385.50, 378.20, 383.75, 800000, "2026-06-25"),
    ("GOOGL", 175.30, 178.90, 174.50, 177.20, 600000, "2026-06-25"),
    ("JPM", 210.50, 213.20, 209.80, 212.10, 500000, "2026-06-25"),
    ("BAC", 42.30, 43.10, 41.90, 42.80, 1200000, "2026-06-25"),
]

columns = ["symbol", "open", "high", "low", "close", "volume", "trade_date"]
df = spark.createDataFrame(data, columns)
df = df.withColumn("ingested_at", current_timestamp())
df = df.withColumn("layer", lit("bronze"))

print("✅ Sample financial data created!")
print(f"Records: {df.count()}")

# Write to Delta Lake (Bronze Layer)
bronze_path = "/tmp/lakehouse/bronze/stock_prices"
df.write.format("delta").mode("overwrite").save(bronze_path)
print(f"✅ Data written to Bronze Delta Lake: {bronze_path}")

# Read back and show
bronze_df = spark.read.format("delta").load(bronze_path)
print("\n📊 Bronze Layer Data:")
bronze_df.show()

# Transform to Silver Layer
silver_df = bronze_df \
    .withColumn("daily_return", 
                (col("close") - col("open")) / col("open") * 100) \
    .withColumn("price_range", col("high") - col("low")) \
    .withColumn("layer", lit("silver"))

silver_path = "/tmp/lakehouse/silver/stock_prices"
silver_df.write.format("delta").mode("overwrite").save(silver_path)
print(f"✅ Data written to Silver Delta Lake: {silver_path}")

# Read Silver and show
silver_df = spark.read.format("delta").load(silver_path)
print("\n📊 Silver Layer Data (with transformations):")
silver_df.select("symbol", "open", "close", "daily_return", "price_range").show()

# Gold Layer - Analytics ready
gold_df = silver_df.groupBy("symbol").agg(
    {"close": "avg", "volume": "sum", "daily_return": "avg"}
).withColumnRenamed("avg(close)", "avg_close") \
 .withColumnRenamed("sum(volume)", "total_volume") \
 .withColumnRenamed("avg(daily_return)", "avg_daily_return") \
 .withColumn("layer", lit("gold"))

gold_path = "/tmp/lakehouse/gold/stock_summary"
gold_df.write.format("delta").mode("overwrite").save(gold_path)
print(f"✅ Data written to Gold Delta Lake: {gold_path}")

print("\n📊 Gold Layer Data (Analytics Ready):")
gold_df.show()

print("\n🎉 Enterprise Data Lakehouse Pipeline Complete!")
print("Layers: Bronze → Silver → Gold")
print("Format: Delta Lake")
print("Engine: Apache Spark")

spark.stop()
