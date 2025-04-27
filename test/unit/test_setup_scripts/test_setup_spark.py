from src.setup_scripts.setup_spark import create_spark_session


def test_create_spark_session():
    spark = create_spark_session("TestIcebergSparkApp")

    # Check that the Spark session is created
    assert spark is not None

    # Check basic config values
    assert (
        spark.conf.get("spark.sql.catalog.local")
        == "org.apache.iceberg.spark.SparkCatalog"
    )
    assert spark.conf.get("spark.sql.catalog.local.type") == "hadoop"
    assert spark.conf.get("spark.sql.catalog.local.warehouse") == "warehouse"

    spark.stop()
