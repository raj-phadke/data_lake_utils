from pyspark.sql import SparkSession


class SetupSpark:
    def __init__(
        self,
        app_name="MySparkApp",
        use_iceberg=False,
        iceberg_catalog_name="local_catalog",
        warehouse_path="file:///tmp/iceberg-warehouse",
        namespace="default",  # Optional namespace parameter
    ):
        self.app_name = app_name
        self.use_iceberg = use_iceberg
        self.iceberg_catalog_name = iceberg_catalog_name
        self.warehouse_path = warehouse_path
        self.namespace = namespace  # Store the namespace
        self.spark = self.create_session()

    def create_session(self):
        builder = (
            SparkSession.builder.appName(self.app_name)
            .master("local[*]")
            .config("spark.sql.shuffle.partitions", "4")
            .config("spark.driver.memory", "4g")
        )

        if self.use_iceberg:
            builder = (
                builder.config(
                    "spark.jars.packages",
                    "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.9.0",
                )
                .config(
                    f"spark.sql.catalog.{self.iceberg_catalog_name}",
                    "org.apache.iceberg.spark.SparkCatalog",
                )
                .config(f"spark.sql.catalog.{self.iceberg_catalog_name}.type", "hadoop")
                .config(
                    f"spark.sql.catalog.{self.iceberg_catalog_name}.warehouse",
                    self.warehouse_path,
                )
                .config(
                    "spark.sql.extensions",
                    "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
                )
                .config(
                    f"spark.sql.catalog.{self.iceberg_catalog_name}.namespace",
                    self.namespace,  # Add the namespace if needed
                )
            )

        self.spark = builder.getOrCreate()
        return self.spark

    def stop_session(self):
        if self.spark:
            self.spark.stop()
            self.spark = None
