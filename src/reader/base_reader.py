from abc import ABC, abstractmethod


from src.connection.base_connection import BaseConnection
from src.configs.dataframe_configs import dataframes


class BaseReader(ABC):
    """
    Abstract Base Reader class that defines the common interface
    for reading data from a source.
    """

    def __init__(self, connection: BaseConnection) -> None:
        """
        Initialize with the connection that has the Spark session.
        """
        self.connection = connection

    @abstractmethod
    def read(self) -> dataframes:
        """
        Abstract method to read data from a source and return a DataFrame.
        """
        pass
