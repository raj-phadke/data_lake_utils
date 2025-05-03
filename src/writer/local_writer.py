from src.writer.base_writer import BaseWriter
from src.connection.local_connection import LocalConnection
from src.configs.dataframe_configs import dataframes


class LocalWriter(BaseWriter):
    def __init__(self, connection: LocalConnection) -> None:
        """
        Initializes the LocalWriter with the connection.

        :param connection: The LocalConnection object that holds connection parameters.
        """
        super().__init__(connection=connection)

    def __write_csv_file(self, df: dataframes) -> None:
        """
        Writes the DataFrame to a CSV file in the specified path.

        :param df: The DataFrame to write.
        """
        output_path = (
            self.connection.params.file_configs.file_path
            + f"/{self.connection.params.file_configs.file_name}.csv"
        )
        df.toPandas().to_csv(output_path, index=False)

    def __write_iceberg_file(self, df: dataframes) -> None:
        """
        Writes the DataFrame to an Iceberg table. If the table doesn't exist, it creates it;
        otherwise, it appends the data.

        :param df: The DataFrame to write to the Iceberg table.
        """
        catalog = self.connection.params.file_configs.catalog_name
        namespace = self.connection.params.file_configs.namespace
        table = self.connection.params.file_configs.file_name

        full_table_name = f"{catalog}.{namespace}.{table}"

        # Check if the table exists
        if self.connection.spark.catalog.tableExists(full_table_name):
            # Table exists, append data
            try:
                df.write.format("iceberg").mode("append").save(full_table_name)
                print(f"Appended to existing Iceberg table: {full_table_name}")
            except Exception as e:
                print(
                    f"Failed to append to Iceberg table: {full_table_name}, Error: {str(e)}"
                )
                raise
        else:
            # Table doesn't exist, create it
            try:
                df.writeTo(full_table_name).using("iceberg").create()
                print(f"Created Iceberg table: {full_table_name}")
            except Exception as e:
                print(
                    f"Failed to create Iceberg table: {full_table_name}, Error: {str(e)}"
                )
                raise

    def write(self, df) -> int:
        """
        Writes the DataFrame to the specified file type (CSV or Iceberg).

        :param df: The DataFrame to write.
        :return: The number of rows written.
        """
        if self.connection.params.file_configs.file_type == "csv":
            self.__write_csv_file(df)
        elif self.connection.params.file_configs.file_type == "iceberg":
            self.__write_iceberg_file(df)
        else:
            raise ValueError(
                f"Unsupported file type: {self.connection.params.file_configs.file_type}"
            )
        return df.count()  # Return the number of rows written
