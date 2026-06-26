import pandas as pd
import pyarrow as pa
import os
from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, StringType, DoubleType, LongType

print("🔍 Initializing Apache Iceberg Pipeline...")

os.makedirs("/tmp/iceberg/warehouse", exist_ok=True)

catalog = SqlCatalog(
    "local",
    **{
        "uri": "sqlite:////tmp/iceberg/catalog.db",
        "warehouse": "/tmp/iceberg/warehouse",
    }
)

print("✅ Iceberg catalog initialized!")

try:
    catalog.create_namespace("lakehouse")
    print("✅ Namespace created!")
except Exception:
    print("✅ Namespace exists!")

schema = Schema(
    NestedField(1, "symbol", StringType(), required=False),
    NestedField(2, "open", DoubleType()),
    NestedField(3, "high", DoubleType()),
    NestedField(4, "low", DoubleType()),
    NestedField(5, "close", DoubleType()),
    NestedField(6, "volume", LongType()),
    NestedField(7, "trade_date", StringType()),
)

try:
    catalog.drop_table("lakehouse.stock_prices")
except Exception:
    pass

table = catalog.create_table("lakehouse.stock_prices", schema=schema)
print("✅ Iceberg table created!")

data = {
    "symbol": ["AAPL", "MSFT", "GOOGL", "JPM", "BAC"],
    "open": [150.25, 380.00, 175.30, 210.50, 42.30],
    "high": [152.80, 385.50, 178.90, 213.20, 43.10],
    "low": [149.10, 378.20, 174.50, 209.80, 41.90],
    "close": [151.50, 383.75, 177.20, 212.10, 42.80],
    "volume": [1000000, 800000, 600000, 500000, 1200000],
    "trade_date": ["2026-06-26"] * 5
}

df = pd.DataFrame(data)
arrow_table = pa.Table.from_pandas(df)

table.append(arrow_table)
print("✅ Data written to Iceberg!")

scan = table.scan()
result = scan.to_arrow()
print(f"\n📊 Iceberg Data ({len(result)} rows):")
print(result.to_pandas().to_string())

print(f"\n📋 Table Metadata:")
print(f"Location: {table.location()}")
print(f"Snapshots: {len(table.snapshots())}")

print("\n🎉 Apache Iceberg Pipeline Complete!")
print("Features: Schema evolution, time travel, ACID transactions")
