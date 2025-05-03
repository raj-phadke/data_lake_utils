from pydantic import BaseModel, model_validator
from typing import Literal, Optional


class FileConfigs(BaseModel):
    file_name: str
    file_path: str
    file_type: Literal["csv", "iceberg", "txt"] = (
        "csv"  # Defaults to CSV, but can be extended to support other types like parquet, json, etc.
    )


class IcebergFileConfigs(FileConfigs):
    catalog_name: str = "local_catalog"  # Catalog name for Iceberg
    warehouse_path: Optional[str] = (
        "file:///tmp/iceberg-warehouse"  # Path to the warehouse
    )
    namespace: str = "default"

    @model_validator(mode="before")
    def check_file_type_is_iceberg(cls, values):
        """
        Validates that the file_type is 'iceberg' if catalog_name is provided.
        """
        file_type = values.get("file_type")
        catalog_name = values.get("catalog_name")

        if catalog_name and file_type != "iceberg":
            raise ValueError(
                "When catalog_name is provided, file_type must be 'iceberg'."
            )

        return values  # Return the validated values dictionary
