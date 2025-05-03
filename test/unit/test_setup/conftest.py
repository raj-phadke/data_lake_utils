import pytest
from src.setup.spark.setup_spark_session import SetupSpark  # Replace with actual path


@pytest.fixture(scope="function")
def basic_spark_session():
    setup = SetupSpark(app_name="TestAppBasic", use_iceberg=False)
    spark = setup.create_session()
    yield spark
    setup.stop_session()


@pytest.fixture(scope="function")
def iceberg_spark_session():
    setup = SetupSpark(
        app_name="TestAppIceberg", use_iceberg=True, iceberg_catalog_name="test_catalog"
    )
    spark = setup.create_session()
    yield spark
    setup.stop_session()
