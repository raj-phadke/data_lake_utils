import pytest
import pandas as pd
from unittest.mock import patch
from src.writer.local_writer import LocalWriter
from src.connection.local_connection import LocalConnection
from src.configs.connection_configs import LocalConnectionParams
from src.configs.file_configs import FileConfigs


@patch("pandas.DataFrame.to_csv")
def test_write_valid_csv(mock_to_csv, valid_connection):
    # Create a mock DataFrame to pass to the write method
    mock_df = pd.DataFrame({"id": [1, 2], "name": ["John", "Jane"]})

    # Mock the behavior of to_csv (it doesn't need to actually do anything)
    mock_to_csv.return_value = (
        None  # We don't need the actual to_csv functionality for the test
    )

    # Create an instance of LocalWriter with the mocked connection
    writer = LocalWriter(valid_connection)

    # Call the write method
    row_count = writer.write(mock_df)

    # Assert that to_csv was called with the correct arguments
    mock_to_csv.assert_called_once_with("/mock/path/mock_file.csv", index=False)

    # Assert that the correct number of rows was returned
    assert row_count == len(mock_df)


@patch("pandas.DataFrame.to_csv")
def test_write_invalid_file_type(mock_to_csv, valid_connection):
    file_configs = FileConfigs(
        file_path="/mock/path",
        file_name="mock_file.txt",
        file_type="txt",
    )

    # Create mock parameters for an invalid file type (e.g., .txt)
    invalid_connection_params = LocalConnectionParams(
        connection_type="target", file_configs=file_configs
    )
    invalid_connection = LocalConnection(invalid_connection_params)

    # Create an instance of LocalWriter with the invalid connection
    writer = LocalWriter(invalid_connection)

    # Create a mock DataFrame
    mock_df = pd.DataFrame({"id": [1, 2], "name": ["John", "Jane"]})

    # Expect a ValueError to be raised when an invalid file type is provided
    with pytest.raises(ValueError):
        writer.write(mock_df)

    # Ensure pandas.DataFrame.to_csv was never called
    mock_to_csv.assert_not_called()
