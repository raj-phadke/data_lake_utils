import pandas as pd
from src.connection.local_connection import LocalConnection
from src.reader.base_reader import BaseReader


class LocalReader(BaseReader):
    def __init__(self, connection: LocalConnection) -> None:
        super().__init__(connection=connection)

    def read(self) -> pd.DataFrame:
        """
        Read data from the local file system and return a PySpark DataFrame.
        """
        if self.connection.params.file_type == "csv":
            return pd.read_csv(
                self.connection.params.file_path
                + f"/{self.connection.params.file_name}"
            )
        else:
            raise ValueError(
                f"Unsupported file type: {self.connection.params.file_type}"
            )
