from abc import ABC, abstractmethod

from pydantic import BaseModel


class BaseConnection(ABC):
    """
    Abstract base class for connections
    """

    def __init__(self, params: BaseModel) -> None:
        self.params = params

    @abstractmethod
    def connect(self) -> None:
        """
        Abstract method to create a connection
        """
