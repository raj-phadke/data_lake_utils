import pytest
from unittest.mock import patch
from src.connection.local_connection import LocalConnection


@patch("os.path.exists")
def test_connect_valid_file(mock_exists, valid_connection_params):
    # Mock that the file exists
    mock_exists.return_value = True

    connection = LocalConnection(valid_connection_params)
    # Expect that the connect method does not raise any exceptions
    try:
        connection.connect()
    except FileNotFoundError:
        pytest.fail("FileNotFoundError raised unexpectedly!")

    # Assert that os.path.exists was called with the correct file path
    mock_exists.assert_called_once_with(valid_connection_params.file_configs.file_path)


@patch("os.path.exists")
def test_connect_invalid_file(mock_exists, invalid_connection_params):
    # Mock that the file does not exist
    mock_exists.return_value = False

    connection = LocalConnection(invalid_connection_params)
    # Expect that FileNotFoundError is raised
    with pytest.raises(FileNotFoundError):
        connection.connect()

    # Assert that os.path.exists was called with the correct file path
    mock_exists.assert_called_once_with(
        invalid_connection_params.file_configs.file_path
    )
