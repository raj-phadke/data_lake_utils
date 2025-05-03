import pytest
import pandas as pd
from unittest.mock import patch
from src.reader.local_reader import LocalReader
from src.connection.local_connection import LocalConnection
from src.configs.connection_configs import LocalConnectionParams


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
def test_read_invalid_file_type(mock_read_csv):
    # Create a mock for an invalid file type (e.g., .txt)
    invalid_connection_params = LocalConnectionParams(
        connection_type="source",
        file_path="/mock/path",
        file_name="mock_file.txt",
        file_type="txt",
    )
    invalid_connection = LocalConnection(invalid_connection_params)

    # Create a reader for the invalid connection (non-CSV file type)
    reader = LocalReader(invalid_connection)

    # Expect that a ValueError is raised when trying to read a non-CSV file
    with pytest.raises(ValueError):
        reader.read()

    # Ensure pandas.read_csv was never called because file type is invalid
    mock_read_csv.assert_not_called()
