from pydantic import BaseModel
from typing import Literal


class FileConfigs(BaseModel):
    file_name: str
    file_path: str
    file_type: Literal["csv", "iceberg", "txt"] = (
        "csv"  # Defaults to CSV, but can be extended to support other types like parquet, json, etc.
    )
