# import pytest
# from unittest.mock import MagicMock
# from src.connection.local_connection import LocalConnection
# from src.writer.local_writer import LocalWriter
# from src.configs.dataframe_configs import dataframes


# @pytest.fixture
# def mock_local_connection():
#     """Fixture to mock LocalConnection"""

#     # Create a mock for LocalConnection
#     mock_connection = MagicMock(spec=LocalConnection)

#     # Mock the params and file_configs structure, make sure it mimics the real object structure
#     mock_connection.params.file_configs = MagicMock()
#     mock_connection.params.file_configs.file_path = "/tmp"
#     mock_connection.params.file_configs.file_name = "test_output"
#     mock_connection.params.file_configs.file_type = "csv"
#     mock_connection.params.file_configs.catalog_name = "local_catalog"
#     mock_connection.params.file_configs.namespace = "default"

#     # Mock the spark catalog methods
#     mock_connection.spark.catalog.tableExists.return_value = False

#     return mock_connection


# @pytest.fixture
# def mock_spark_dataframe():
#     """Fixture to mock a Spark DataFrame"""
#     mock_df = MagicMock(spec=dataframes)
#     mock_df.count.return_value = 5  # Return 5 rows when df.count() is called
#     return mock_df


# @pytest.fixture
# def local_writer(mock_local_connection):
#     """Fixture to instantiate LocalWriter"""
#     return LocalWriter(connection=mock_local_connection)
