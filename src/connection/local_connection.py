import os

from src.configs.connection_configs import LocalConnectionParams
from src.connection.base_connection import BaseConnection


class LocalConnection(BaseConnection):
    """
    Concrete class for local file system connection.
    """

    def __init__(self, params: LocalConnectionParams) -> None:
        super().__init__(params=params)

    def connect(self) -> "LocalConnection":
        """
        Connect to local file system (Mac/Windows)
        Here you can validate the file path exists and can be read.
        """
        if not os.path.exists(self.params.file_path):
            raise FileNotFoundError(f"File at {self.params.file_path} not found.")
        print(f"Connected to local file: {self.params.file_path}")
        return self
