import pandas as pd

file_path = "MOSFET_ID_VDS.csv"
df = pd.read_csv(file_path)
print(df.columns)
print(df.shape)
print(df.describe())
