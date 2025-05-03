from abc import ABC, abstractmethod


from src.connection.base_connection import BaseConnection
from src.configs.dataframe_configs import dataframes


class BaseWriter(ABC):
    """
    Abstract Base Writer class that defines the common interface
    for writing data to a destination.
    """

    def __init__(self, connection: BaseConnection) -> None:
        """
        Initialize with the connection that has the Spark session.
        """
        self.connection = connection

    @abstractmethod
    def write(self, df: dataframes) -> int:
        """
        Abstract method to write a DataFrame to a destination.
        """
        pass
