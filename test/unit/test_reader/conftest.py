import pytest
from src.connection.local_connection import LocalConnection
from src.configs.connection_configs import LocalConnectionParams


@pytest.fixture
def valid_connection_params():
    # Mock parameters for a valid CSV file
    return LocalConnectionParams(
        connection_type="source",
        file_path="/mock/path",
        file_name="mock_file.csv",
        file_type="csv",
    )


@pytest.fixture
def valid_connection(valid_connection_params):
    # Create a LocalConnection object with valid parameters
    connection = LocalConnection(valid_connection_params)
    return connection
