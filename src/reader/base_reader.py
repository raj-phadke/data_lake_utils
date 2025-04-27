from abc import ABC, abstractmethod

import pandas as pd

from src.connection.base_connection import BaseConnection


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
    def read(self) -> pd.DataFrame:
        """
        Abstract method to read data from a source and return a PySpark DataFrame.
        """
        pass
