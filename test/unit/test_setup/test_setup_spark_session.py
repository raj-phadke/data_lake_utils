def test_basic_spark_session(basic_spark_session):
    spark = basic_spark_session
    assert spark.sparkContext.appName == "MySparkApp"
    assert spark.sparkContext.getConf().get("spark.master") == "local[*]"


def test_iceberg_spark_session(iceberg_spark_session):
    spark = iceberg_spark_session
    conf = spark.sparkContext.getConf()
    assert (
        conf.get("spark.jars.packages")
        == "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.9.0"
    )
    assert (
        conf.get("spark.sql.catalog.test_catalog")
        == "org.apache.iceberg.spark.SparkCatalog"
    )
    assert conf.get("spark.sql.catalog.test_catalog.type") == "hadoop"
    assert (
        conf.get("spark.sql.catalog.test_catalog.warehouse")
        == "file:///tmp/iceberg-warehouse"
    )
    assert (
        conf.get("spark.sql.extensions")
        == "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
    )
