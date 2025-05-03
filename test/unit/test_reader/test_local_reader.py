import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.reader.local_reader import LocalReader
from src.configs.connection_configs import LocalConnectionParams
from src.configs.file_configs import FileConfigs
from pyspark.sql import DataFrame


# Mock configuration for LocalConnectionParams
@pytest.fixture
def valid_connection_params():
    # Provide a valid configuration for CSV
    return LocalConnectionParams(
        connection_type="source",
        file_configs=FileConfigs(
            file_type="csv", file_path="/mock/path", file_name="valid_file.csv"
        ),
    )


@pytest.fixture
def iceberg_connection():
    # Provide a configuration for Iceberg file type

    return LocalConnectionParams(
        connection_type="source",
        file_configs=FileConfigs(
            file_type="iceberg", file_path="/mock/iceberg/path", file_name="mock_table"
        ),
    )


@patch("pandas.read_csv")
def test_read_valid_csv(mock_read_csv, valid_connection):
    # Mock the returned value of read_csv
    mock_df = pd.DataFrame({"id": [1, 2], "name": ["John", "Jane"]})
    mock_read_csv.return_value = mock_df

    # Initialize LocalReader with the mocked connection
    reader = LocalReader(valid_connection)

    # Run the read method and get the dataframe
    df = reader.read()

    # Assert that pandas read_csv was called correctly
    mock_read_csv.assert_called_once_with("/mock/path/mock_file.csv")

    # Assert the returned DataFrame is correct
    pd.testing.assert_frame_equal(df, mock_df)


@patch("pandas.read_csv")
@patch.object(LocalReader, "__read_csv_file")
def test_read_invalid_file_type(mock_read_csv, mock_read_csv_file, invalid_connection):
    # Mock that the read method will not be called as it's an invalid type
    mock_read_csv.return_value = None
    mock_read_csv_file.return_value = None

    # Initialize the reader with the invalid connection (non-CSV file type)
    reader = LocalReader(invalid_connection)

    # Expect that a ValueError is raised when trying to read a non-CSV file
    with pytest.raises(ValueError):
        reader.read()

    # Ensure pandas.read_csv was never called
    mock_read_csv.assert_not_called()
    mock_read_csv_file.assert_not_called()


@patch("pyspark.sql.DataFrame")
@patch.object(LocalReader, "__read_iceberg_file")
def test_read_iceberg_file(mock_read_iceberg_file, mock_spark_df, iceberg_connection):
    # Create a mock Spark DataFrame
    mock_spark_df = MagicMock(spec=DataFrame)
    mock_read_iceberg_file.return_value = mock_spark_df

    # Initialize the reader with the iceberg connection
    reader = LocalReader(iceberg_connection)

    # Run the read method and get the Spark DataFrame
    df = reader.read()

    # Assert that the iceberg read method was called correctly
    mock_read_iceberg_file.assert_called_once()

    # Assert that the returned Spark DataFrame is correct
    assert df == mock_spark_df


@patch("pandas.read_csv")
@patch("pyspark.sql.DataFrame")
def test_read_unsupported_file_type(mock_spark_df, mock_read_csv, valid_connection):
    # Set an unsupported file type
    valid_connection.params.file_configs.file_type = "unsupported"

    # Initialize the reader with the invalid file type
    reader = LocalReader(valid_connection)

    # Expect a ValueError to be raised for unsupported file type
    with pytest.raises(ValueError):
        reader.read()

    # Ensure pandas.read_csv and spark.read were never called
    mock_read_csv.assert_not_called()
    mock_spark_df.assert_not_called()
