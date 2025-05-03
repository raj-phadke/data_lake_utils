import pytest
from src.configs.connection_configs import LocalConnectionParams
from src.configs.file_configs import FileConfigs


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
def invalid_connection_params():
    # Provide an invalid configuration for CSV (non-existent file)
    return LocalConnectionParams(
        connection_type="source",
        file_configs=FileConfigs(
            file_type="csv", file_path="/mock/path", file_name="invalid_file.csv"
        ),
    )


@pytest.fixture
def iceberg_connection_params():
    # Provide a configuration for Iceberg file type

    return LocalConnectionParams(
        connection_type="source",
        file_configs=FileConfigs(
            file_type="iceberg", file_path="/mock/iceberg/path", file_name="mock_table"
        ),
    )
