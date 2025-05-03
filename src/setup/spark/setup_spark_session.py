from pyspark.sql import SparkSession


class SetupSpark:
    def __init__(
        self,
        app_name="MySparkApp",
        use_iceberg=False,
        iceberg_catalog_name="local_catalog",
    ):
        self.app_name = app_name
        self.use_iceberg = use_iceberg
        self.iceberg_catalog_name = iceberg_catalog_name
        self.spark = None

    def create_session(self):
        builder = (
            SparkSession.builder.appName(self.app_name)
            .master("local[*]")
            .config("spark.sql.shuffle.partitions", "4")
            .config("spark.driver.memory", "4g")
        )

        if self.use_iceberg:
            # Iceberg JAR for Spark 3.3 and Scala 2.12
            iceberg_package = "org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.4.2"

            builder = (
                builder.config("spark.jars.packages", iceberg_package)
                .config(
                    f"spark.sql.catalog.{self.iceberg_catalog_name}",
                    "org.apache.iceberg.spark.SparkCatalog",
                )
                .config(f"spark.sql.catalog.{self.iceberg_catalog_name}.type", "hadoop")
                .config(
                    f"spark.sql.catalog.{self.iceberg_catalog_name}.warehouse",
                    "file:///tmp/iceberg-warehouse",
                )
                .config(
                    "spark.sql.extensions",
                    "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
                )
            )

        self.spark = builder.getOrCreate()
        return self.spark

    def stop_session(self):
        if self.spark:
            self.spark.stop()
            self.spark = None
