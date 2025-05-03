import pytest
from src.configs.connection_configs import LocalConnectionParams
from src.configs.file_configs import FileConfigs


@pytest.fixture
def valid_connection_params():
    # Mock parameters where the file exists
    return LocalConnectionParams(
        connection_type="source",
        file_configs=FileConfigs(
            file_name="sample_read.csv",
            file_path="/Users/raj-phadke/Desktop/personal_projects/data_lake_utils",
            file_type="csv",
        ),
    )


@pytest.fixture
def invalid_connection_params():
    # Mock parameters where the file does not exist
    return LocalConnectionParams(
        connection_type="source",
        file_configs=FileConfigs(
            file_name="sample_write.csv",
            file_path="/Users/raj-phadke/Desktop/personal_projects/data_lake_utils",
            file_type="csv",
        ),
    )
