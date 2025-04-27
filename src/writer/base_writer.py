from abc import ABC, abstractmethod

import pandas as pd

from src.connection.base_connection import BaseConnection


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
    def write(self, df: pd.DataFrame) -> int:
        """
        Abstract method to write a PySpark DataFrame to a destination.
        """
        pass
