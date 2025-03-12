import pandas as pd

url = "https://raw.githubusercontent.com/seung-m1nsong/Data698/refs/heads/main/product_info.csv"

df = pd.read_csv(url)

print(df.head())
