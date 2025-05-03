import pytest
from unittest.mock import patch
from src.connection.local_connection import LocalConnection
import os


@patch("os.path.exists")
def test_connect_valid_file(mock_exists, valid_connection_params):
    # Mock that the file exists
    mock_exists.return_value = True

    # Initialize the connection with valid params
    connection = LocalConnection(valid_connection_params)

    # Expect that the connect method does not raise any exceptions
    try:
        connection.connect()
    except FileNotFoundError:
        pytest.fail("FileNotFoundError raised unexpectedly!")

    # Assert that os.path.exists was called with the correct file path
    file_path = os.path.join(
        valid_connection_params.file_configs.file_path,
        valid_connection_params.file_configs.file_name,
    )
    mock_exists.assert_called_once_with(file_path)


@patch("os.path.exists")
@patch("os.listdir")
def test_connect_valid_iceberg_file(
    mock_listdir, mock_exists, iceberg_connection_params
):
    # Mock the existence of Iceberg directories and metadata files
    mock_exists.side_effect = lambda path: path in [
        "/mock/iceberg/path/metadata",
        "/mock/iceberg/path/data",
    ]
    mock_listdir.return_value = ["manifest", "metadata.json"]

    # Initialize the connection with Iceberg params
    connection = LocalConnection(iceberg_connection_params)

    # Expect that the connect method works without raising any exceptions
    connection.connect()

    # Assert that os.path.exists was called for metadata and data directories
    mock_exists.assert_any_call("/mock/iceberg/path/metadata")
    mock_exists.assert_any_call("/mock/iceberg/path/data")

    # Assert that os.listdir was called for the metadata directory
    mock_listdir.assert_called_once_with("/mock/iceberg/path/metadata")


@patch("os.path.exists")
@patch("os.listdir")
def test_connect_invalid_iceberg_file(
    mock_listdir, mock_exists, iceberg_connection_params
):
    # Mock that the Iceberg metadata directory exists but has no metadata files
    mock_exists.side_effect = lambda path: path in [
        "/mock/iceberg/path/metadata",
        "/mock/iceberg/path/data",
    ]
    mock_listdir.return_value = []  # No metadata files

    # Initialize the connection with Iceberg params
    connection = LocalConnection(iceberg_connection_params)

    # Expect that no metadata files will trigger a warning
    connection.connect()

    # Assert that os.path.exists was called for metadata and data directories
    mock_exists.assert_any_call("/mock/iceberg/path/metadata")
    mock_exists.assert_any_call("/mock/iceberg/path/data")

    # Assert that os.listdir was called for the metadata directory
    mock_listdir.assert_called_once_with("/mock/iceberg/path/metadata")


@patch("os.path.exists")
def test_connect_unsupported_file_type(mock_exists, valid_connection_params):
    # Mock that the file exists
    mock_exists.return_value = True

    # Set an unsupported file type
    valid_connection_params.file_configs.file_type = "unsupported"

    # Initialize the connection with the unsupported file type
    connection = LocalConnection(valid_connection_params)

    # Expect the logger to log an error message for unsupported file type
    with patch.object(connection.logger, "error") as mock_logger_error:
        connection.connect()
        mock_logger_error.assert_called_once_with("Unsupported file type: unsupported")
