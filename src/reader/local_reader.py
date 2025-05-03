from src.connection.local_connection import LocalConnection
from src.reader.base_reader import BaseReader
from src.configs.dataframe_configs import dataframes
import os


class LocalReader(BaseReader):
    def __init__(self, connection: LocalConnection) -> None:
        super().__init__(connection=connection)

    def __read_csv_file(self) -> dataframes:
        file_path = os.path.join(
            self.connection.params.file_configs.file_path,
            self.connection.params.file_configs.file_name,
        )
        return (
            self.connection.spark.read.option("header", True)
            .option("inferSchema", True)
            .csv(file_path)
        )

    def __read_iceberg_file(self) -> dataframes:
        # Reading the Iceberg table
        iceberg_table_path = f"{self.connection.params.file_configs.file_path}/{self.connection.params.file_configs.file_name}"

        # Read the Iceberg table into a Spark DataFrame
        spark_df = self.connection.spark.read.format("iceberg").load(iceberg_table_path)

        return spark_df

    def read(self) -> dataframes:
        """
        Read data from the local file system and return a PySpark DataFrame.
        """
        if self.connection.params.file_configs.file_type == "csv":
            return self.__read_csv_file()
        elif self.connection.params.file_configs.file_type == "iceberg":
            return self.__read_iceberg_file()
        else:
            raise ValueError(
                f"Unsupported file type: {self.connection.params.file_configs.file_type}"
            )
