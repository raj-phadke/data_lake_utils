import pandas as pd

from src.connection.local_connection import LocalConnection
from src.writer.base_writer import BaseWriter


class LocalWriter(BaseWriter):
    def __init__(self, connection: LocalConnection) -> None:
        super().__init__(connection=connection)

    def write(self, df: pd.DataFrame) -> int:
        """
        Write the PySpark DataFrame to a local file system.
        """
        if self.connection.params.file_type == "csv":
            df.to_csv(
                self.connection.params.file_path
                + f"/{self.connection.params.file_name}",
                index=False,
            )
        else:
            raise ValueError(
                f"Unsupported file type: {self.connection.params.file_type}"
            )
        print(df.count())
        return df.count()
