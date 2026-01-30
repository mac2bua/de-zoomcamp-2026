import pandas as pd


month = 12
df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df['month'] = month
print(df.head())

df.to_parquet(f"output_{month}.parquet")