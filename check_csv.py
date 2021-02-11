import pandas as pd
df=pd.read_csv('file-name.csv',header=None)
df.to_csv("file-name.csv", header=["date", "tweet", "user","place"], index=False)
df = pd.read_csv("file-name.csv", usecols = ['tweet'])
print(df['tweet'][2])
