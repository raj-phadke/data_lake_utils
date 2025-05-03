from src.configs.connection_configs import LocalConnectionParams
from src.configs.file_configs import FileConfigs
from src.connection.local_connection import LocalConnection
from src.reader.local_reader import LocalReader
from src.writer.local_writer import LocalWriter

source_file_configs = FileConfigs(
    file_path="/Users/raj-phadke/Desktop/personal_projects/data_lake_utils/",
    file_name="sample_read.csv",
    file_type="csv",
)

target_file_configs = FileConfigs(
    file_path="/Users/raj-phadke/Desktop/personal_projects/data_lake_utils/",
    file_name="sample_write.csv",
    file_type="csv",
)

# Setup source location params
local_source_connection_params = LocalConnectionParams(
    connection_type="source", file_configs=source_file_configs
)

# Setup target location params
local_target_connection_params = LocalConnectionParams(
    connection_type="target", file_configs=target_file_configs
)

# Setup source local connection
source_connection = LocalConnection(params=local_source_connection_params).connect()
# Setup target local connection
target_connection = LocalConnection(params=local_target_connection_params).connect()


reader = LocalReader(connection=source_connection)
writer = LocalWriter(connection=target_connection)

df = reader.read()
print(df)

print("\nAttempting to write\n")
writer.write(df=df)
