from pydantic import BaseModel
from typing import Literal
from src.configs.file_configs import FileConfigs


class LocalConnectionParams(BaseModel):
    """
    Parameters for connecting to local files.
    """

    connection_type: Literal["source", "target"]
    file_configs: FileConfigs
