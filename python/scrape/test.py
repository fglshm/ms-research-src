import pandas as pd

df = pd.read_csv('test.csv', header=None)
print(df)
df = df.drop(1)
print(df)
df = df.append({0: 6, 1: 60}, ignore_index=True)
print(df)
# df.to_csv('test.csv', header=None, index=False)
