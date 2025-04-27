from pydantic import BaseModel
from typing import Literal


class LocalConnectionParams(BaseModel):
    """
    Parameters for connecting to local files.
    """

    connection_type: Literal["source", "target"]
    file_path: str
    file_name: str
    file_type: str = "csv"  # Defaults to CSV, but can be extended to support other types like parquet, json, etc.
