from src.setup.spark.setup_spark_session import SetupSpark
from src.connection.local_connection import (
    LocalConnectionParams,
    LocalConnection,
)
from src.configs.file_configs import IcebergFileConfigs
from src.writer.local_writer import LocalWriter
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql import Row

# Step 1: Set up Spark with Iceberg
spark_setup = SetupSpark(
    use_iceberg=True,
    iceberg_catalog_name="local_catalog",
    warehouse_path="file:///tmp/iceberg-warehouse",
)
spark = spark_setup.spark

# Step 2: Create test data
data = [Row(id="11", name="Cristiano Jack", age="57", city="Boston")]
schema = StructType(
    [
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("age", StringType(), True),
        StructField("city", StringType(), True),
    ]
)
df = spark.createDataFrame(data, schema=schema)

# Step 3: Connection configuration
file_configs = IcebergFileConfigs(
    file_type="iceberg",
    file_name="sample_iceberg_write",
    file_path="/tmp",
    catalog_name="local_catalog",
    namespace="default",
)
params = LocalConnectionParams(connection_type="target", file_configs=file_configs)
connection = LocalConnection(params=params)

# Step 4: Write the data
writer = LocalWriter(connection=connection)
writer.write(df)

# Step 5: Stop Spark
spark_setup.stop_session()
