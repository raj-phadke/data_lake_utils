from pyspark.sql import SparkSession


def create_spark_session(app_name="IcebergSparkApp"):
    spark = (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.iceberg.spark.SparkSessionCatalog",
        )
        .config("spark.sql.catalog.spark_catalog.type", "hive")
        .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.local.type", "hadoop")
        .config("spark.sql.catalog.local.warehouse", "warehouse")
        .getOrCreate()
    )

    return spark


if __name__ == "__main__":
    spark = create_spark_session()
    print("Spark session created with Iceberg support.")
    spark.stop()
