import pandas as pd

url = "https://raw.githubusercontent.com/seung-m1nsong/Data698/refs/heads/main/DataWeb-Query-Export.csv"
df = pd.read_csv(url, skiprows=2)

if 'Data Type' in df.columns:
    del df['Data Type']

numeric_cols = ["Year", "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"]

df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

df[numeric_cols] = df[numeric_cols].fillna(0).astype(int)

print(df.head())

#output_file_path = r"C:\Users\SeungminSong\Downloads\698_Research\imports.csv"
#df.to_csv(output_file_path, index=False)

selected_countries = ["Australia", "France", "Japan", "South Korea", "United Kingdom"]

df_filtered = df[df["Country"].isin(selected_countries)]


df_grouped = df_filtered.groupby(["Year", "Country"]).sum().reset_index()

df_grouped["Total"] = df_grouped[
    ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"]
].astype(float).sum(axis=1).astype(int)

df_grouped = df_grouped.iloc[:-1]

#print(df_grouped)

country_totals = df_grouped.groupby("Country")["Total"].sum().reset_index()

country_totals = country_totals.sort_values(by="Total", ascending=False)

print(country_totals.head())

pivot_df = df_grouped.pivot(index="Year", columns="Country", values=df_grouped.columns[2:]).fillna(0)

print(pivot_df)

