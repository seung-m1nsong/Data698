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

from IPython.display import display

display(country_totals.head())

# Convert Year-by-Country data to a PivotTable to compare country values ​​for each year.
pivot_df = df_grouped.pivot(index="Year", columns="Country", values=df_grouped.columns[2:]).fillna(0)
print(pivot_df)


df_melted = df_grouped.melt(id_vars=["Country", "Year"], 
                    var_name="Month", 
                    value_name="Value")

df_melted["Date"] = df_melted["Year"].astype(str) + "-" + df_melted["Month"].str[:3]
df_melted = df_melted.drop(columns=["Year", "Month"])

display(df_melted.head())

#output_file_path = r"C:\Users\SeungminSong\Downloads\698_Research\imports_pivot2.csv"
#df_melted.to_csv(output_file_path, index=False)

# Monthly exchange rate. South Korea Won to USD
url = "https://raw.githubusercontent.com/seung-m1nsong/Data698/refs/heads/main/EXKOUS.csv"
df_kor = pd.read_csv(url)

df_kor.rename(columns={"observation_date": "Date", "EXKOUS": "Kor_rate"}, inplace=True)

df_kor["Date"] = pd.to_datetime(df_kor["Date"])

df_kor["Year-Month"] = df_kor["Date"].dt.strftime("%Y-%b")

df_kor = df_kor.drop(columns=["Date"])
df_kor.rename(columns={"Year-Month": "Date"}, inplace=True)

df_kor = df_kor[["Date", "Kor_rate"]]
display(df_kor.head())

missing_values = df_kor.isnull().sum()

missing_values = missing_values[missing_values > 0]

print(missing_values)

url = "https://raw.githubusercontent.com/seung-m1nsong/Data698/refs/heads/main/Crude%20Oil%20WTI%20Futures%20Historical%20Data.csv"
df_oil = pd.read_csv(url)

df_oil = df_oil.drop(columns=["Open", "High", "Low", "Vol.", "Change %"])

df_oil["Date"] = pd.to_datetime(df_oil["Date"]).dt.strftime("%Y-%b")

df_oil["Date"] = pd.to_datetime(df_oil["Date"], format="%Y-%b")
df_oil = df_oil.sort_values(by="Date", ascending=True)  # 오래된 날짜가 위로, 최신 날짜가 아래로

df_oil["Date"] = df_oil["Date"].dt.strftime("%Y-%b")
display(df_oil.head())

#output_file_path = r"C:\Users\SeungminSong\Downloads\698_Research\oil.csv"
#df_oil.to_csv(output_file_path, index=False)

# Energy Consumption Data Refinement and Processing

url = "https://raw.githubusercontent.com/seung-m1nsong/Data698/refs/heads/main/Primary_Energy_Overview.csv"
df_energy = pd.read_csv(url)

df_energy = df_energy[df_energy["Month"].notna()].reset_index(drop=True)

df_energy.rename(columns={"Month": "Date", "Total Primary Energy Consumption": "Total"}, inplace=True)

df_energy["Date"] = df_energy["Date"].str.replace(r"\?\?", "", regex=True).str.strip()

df_energy["Date"] = pd.to_datetime(df_energy["Date"], format="%Y %m", errors="coerce")

df_energy["Year-Month"] = df_energy["Date"].dt.strftime("%Y-%b")

df_energy.drop(columns=["Date"], inplace=True)

df_energy = df_energy.rename(columns={"Year-Month": "Date"})
cols = ["Date"] + [col for col in df_energy.columns if col != "Date"]
df_energy = df_energy[cols]

df_energy = df_energy[["Date", "Total"]]
display(df_energy.head())
