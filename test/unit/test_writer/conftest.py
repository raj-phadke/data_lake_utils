import pytest
from src.connection.local_connection import LocalConnection
from src.configs.connection_configs import LocalConnectionParams
from src.configs.file_configs import FileConfigs


@pytest.fixture
def mock_file_config_params():
    return FileConfigs(
        file_path="/mock/path",
        file_name="mock_file.csv",
        file_type="csv",
    )


@pytest.fixture
def valid_connection_params(mock_file_config_params):
    # Mock parameters for a valid CSV file
    return LocalConnectionParams(
        connection_type="target", file_configs=mock_file_config_params
    )


@pytest.fixture
def valid_connection(valid_connection_params):
    # Create a LocalConnection object with valid parameters
    connection = LocalConnection(valid_connection_params)
    return connection
