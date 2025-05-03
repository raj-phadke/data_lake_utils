import logging
from abc import ABC, abstractmethod
from pydantic import BaseModel

# Configure logging once, at the top level
logging.basicConfig(level=logging.INFO)


class BaseConnection(ABC):
    """
    Abstract base class for connections
    """

    def __init__(self, params: BaseModel) -> None:
        self.params = params
        self.logger = logging.getLogger(__name__)  # Proper logger usage

    @abstractmethod
    def connect(self) -> None:
        """
        Abstract method to create a connection
        """
        pass
