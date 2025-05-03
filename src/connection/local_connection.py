import os

from src.configs.connection_configs import LocalConnectionParams
from src.connection.base_connection import BaseConnection
from src.setup.spark.setup_spark_session import SetupSpark


class LocalConnection(BaseConnection):
    """
    Concrete class for local file system connection.
    """

    def __init__(self, params: LocalConnectionParams) -> None:
        super().__init__(params=params)
        use_iceberg = False
        if params.file_configs.file_type == "iceberg":
            use_iceberg = True

        self.spark = SetupSpark(use_iceberg=use_iceberg).spark

    def connect(self) -> "LocalConnection":
        """
        Connect to local file system (Mac/Windows) and validate the existence of files.
        """
        file_type = self.params.file_configs.file_type

        if file_type == "csv":
            # For CSV files, check if the file exists
            file_path = os.path.join(
                self.params.file_configs.file_path, self.params.file_configs.file_name
            )
            if not os.path.exists(file_path):
                self.logger.error(f"CSV file not found at {file_path}.")
            else:
                self.logger.info(f"Connected to CSV file: {file_path}")

        elif file_type == "iceberg":
            metadata_dir = os.path.join(self.params.file_configs.file_path, "metadata")
            if not os.path.exists(metadata_dir):
                self.logger.warning(
                    f"Iceberg metadata directory not found at {metadata_dir}."
                )
            else:
                # Check for metadata files (e.g., 'manifest' or 'metadata.json')
                metadata_files = [
                    f
                    for f in os.listdir(metadata_dir)
                    if f.startswith("manifest") or f.endswith(".json")
                ]
                if not metadata_files:
                    self.logger.warning(
                        f"No Iceberg metadata files found in: {metadata_dir}."
                    )
                else:
                    self.logger.info(f"Metadata files found in: {metadata_dir}")

            # Optionally verify data directory
            data_dir = os.path.join(self.params.file_configs.file_path, "data")
            if not os.path.exists(data_dir):
                self.logger.warning(f"Iceberg data directory not found at {data_dir}.")
            else:
                self.logger.info(f"Iceberg data directory exists: {data_dir}")

            self.logger.info(
                f"Checked Iceberg table at: {self.params.file_configs.file_path}"
            )

        else:
            self.logger.error(f"Unsupported file type: {file_type}")

        return self
