import pytest
from unittest.mock import MagicMock, patch
from src.writer.local_writer import LocalWriter
from src.connection.local_connection import LocalConnection
from src.configs.dataframe_configs import dataframes

# Fixtures


@pytest.fixture
def mock_local_connection():
    # Creating a mock LocalConnection instance
    mock_connection = MagicMock(spec=LocalConnection)
    mock_connection.params.file_configs.file_type = "csv"  # Default to 'csv'
    mock_connection.params.file_configs.file_path = "/mock/path"
    mock_connection.params.file_configs.file_name = "mock_file"
    return mock_connection


@pytest.fixture
def local_writer(mock_local_connection):
    # Instantiate the LocalWriter with a mock connection
    return LocalWriter(connection=mock_local_connection)


@pytest.fixture
def mock_iceberg_local_connection():
    # Creating a mock LocalConnection for Iceberg
    mock_connection = MagicMock(spec=LocalConnection)
    mock_connection.params.file_configs.file_type = "iceberg"
    mock_connection.params.file_configs.file_path = "/mock/iceberg/path"
    mock_connection.params.file_configs.file_name = "mock_table"
    mock_connection.params.file_configs.catalog_name = "mock_catalog"
    mock_connection.params.file_configs.namespace = "mock_namespace"
    return mock_connection


@pytest.fixture
def local_writer_iceberg(mock_iceberg_local_connection):
    # Instantiate the LocalWriter with a mock connection for Iceberg
    return LocalWriter(connection=mock_iceberg_local_connection)


# Test CSV file writing functionality


def test_write_csv_file(local_writer, mock_local_connection):
    # Mock the pandas to_csv method to avoid actual file writing
    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        mock_df = MagicMock(spec=dataframes)  # Mock the DataFrame
        local_writer._LocalWriter__write_csv_file(mock_df)

        # Check that to_csv was called with the expected file path
        expected_file_path = "/mock/path/mock_file.csv"
        mock_to_csv.assert_called_once_with(expected_file_path, index=False)


# Test Iceberg file writing functionality (Create Table)


def test_write_iceberg_file_create(local_writer_iceberg, mock_iceberg_local_connection):
    # Mock the spark catalog and tableExists method for creating Iceberg table
    with patch.object(
        local_writer_iceberg.connection.spark.catalog, "tableExists", return_value=False
    ) as mock_table_exists:
        with patch("src.writer.local_writer.DataFrame.writeTo") as mock_write_to:
            mock_df = MagicMock(spec=dataframes)  # Mock the DataFrame

            # Call the method to test
            local_writer_iceberg._LocalWriter__write_iceberg_file(mock_df)

            # Check that the create method was called on the iceberg table
            expected_table_name = "mock_catalog.mock_namespace.mock_table"
            mock_write_to.assert_called_once_with(expected_table_name)
            mock_write_to.return_value.using.assert_called_once_with("iceberg")
            mock_write_to.return_value.create.assert_called_once()


# Test Iceberg file writing functionality (Append Data)


def test_write_iceberg_file_append(local_writer_iceberg, mock_iceberg_local_connection):
    # Mock the spark catalog and tableExists method for appending to an Iceberg table
    with patch.object(
        local_writer_iceberg.connection.spark.catalog, "tableExists", return_value=True
    ) as mock_table_exists:
        with patch("src.writer.local_writer.DataFrame.write") as mock_write:
            mock_df = MagicMock(spec=dataframes)  # Mock the DataFrame

            # Call the method to test
            local_writer_iceberg._LocalWriter__write_iceberg_file(mock_df)

            # Check that the append method was called on the iceberg table
            expected_table_name = "mock_catalog.mock_namespace.mock_table"
            mock_write.assert_called_once_with()
            mock_write.return_value.format.assert_called_once_with("iceberg")
            mock_write.return_value.mode.assert_called_once_with("append")
            mock_write.return_value.save.assert_called_once_with(expected_table_name)


# Test general write method for CSV


def test_write_csv(local_writer, mock_local_connection):
    mock_df = MagicMock(spec=dataframes)
    # Mock the method to write CSV
    with patch.object(local_writer, "_LocalWriter__write_csv_file") as mock_write_csv:
        local_writer.write(mock_df)
        # Check if the write CSV method was called
        mock_write_csv.assert_called_once_with(mock_df)


# Test general write method for Iceberg


def test_write_iceberg(local_writer_iceberg, mock_iceberg_local_connection):
    mock_df = MagicMock(spec=dataframes)
    # Mock the method to write Iceberg files
    with patch.object(
        local_writer_iceberg, "_LocalWriter__write_iceberg_file"
    ) as mock_write_iceberg:
        local_writer_iceberg.write(mock_df)
        # Check if the write Iceberg method was called
        mock_write_iceberg.assert_called_once_with(mock_df)


# Test unsupported file type


def test_write_unsupported_file_type(local_writer, mock_local_connection):
    mock_df = MagicMock(spec=dataframes)
    # Set the file type to something unsupported
    mock_local_connection.params.file_configs.file_type = "unsupported"

    # Call the write method and check for ValueError
    with pytest.raises(ValueError, match="Unsupported file type"):
        local_writer.write(mock_df)


# Test connection to the CSV file in LocalConnection


def test_connect_to_csv(mock_local_connection):
    with patch("os.path.exists", return_value=True) as mock_exists:
        mock_connection = mock_local_connection
        mock_connection.connect()
        # Check if the correct log message for connection is triggered
        mock_connection.logger.info.assert_called_with(
            "Connected to CSV file: /mock/path/mock_file"
        )


# Test connection to Iceberg in LocalConnection


def test_connect_to_iceberg(mock_iceberg_local_connection):
    with patch("os.path.exists", return_value=True) as mock_exists:
        mock_connection = mock_iceberg_local_connection
        mock_connection.connect()
        # Check if the correct log message for Iceberg connection is triggered
        mock_connection.logger.info.assert_called_with(
            "Checked Iceberg table at: /mock/iceberg/path"
        )


# Test file not found for CSV


def test_csv_file_not_found(mock_local_connection):
    with patch("os.path.exists", return_value=False) as mock_exists:
        mock_connection = mock_local_connection
        mock_connection.connect()
        # Check that the correct log warning is triggered
        mock_connection.logger.error.assert_called_with(
            "CSV file not found at /mock/path/mock_file"
        )
