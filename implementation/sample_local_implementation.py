from src.configs.connection_configs import LocalConnectionParams
from src.connection.local_connection import LocalConnection
from src.reader.local_reader import LocalReader
from src.writer.local_writer import LocalWriter

# Setup source location params
local_source_connection_params = LocalConnectionParams(
    connection_type="source",
    file_path="/Users/raj-phadke/Desktop/personal_projects/data_lake_utils/",
    file_name="sample_read.csv",
    file_type="csv",
)

# Setup target location params
local_target_connection_params = LocalConnectionParams(
    connection_type="target",
    file_path="/Users/raj-phadke/Desktop/personal_projects/data_lake_utils/",
    file_name="sample_write.csv",
    file_type="csv",
)

# Setup source local connection
source_connection = LocalConnection(params=local_source_connection_params).connect()
# Setup target local connection
target_connection = LocalConnection(params=local_target_connection_params).connect()


reader = LocalReader(connection=source_connection)
writer = LocalWriter(connection=target_connection)

df = reader.read()
print(df)

# New sample row to be added
new_row = {"id": 11, "name": "Cristiano Jack", "age": 57, "city": "Boston"}

# Adding the new row
df.loc[len(df)] = new_row  # Adds the new row at the end of the DataFrame

print("\nDf after adding new row\n")
print(df)

print("\nAttemption to write\n")
writer.write(df=df)
