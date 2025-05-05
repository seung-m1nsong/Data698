# %%
# 1. Open trade data

import pandas as pd
import os

url = "https://raw.githubusercontent.com/seung-m1nsong/Data698/refs/heads/main/DataWeb-Query-Export%20(3).csv"
df = pd.read_csv(url, skiprows=2)

if 'Data Type' in df.columns:
    del df['Data Type']

numeric_cols = ["Year", "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

df[numeric_cols] = df[numeric_cols].fillna(0).astype(int)

print(df.head())

# %%
# 2. Filter specific countries and calculate annual totals

selected_countries = ["Australia", "France", "Japan", "South Korea", "United Kingdom"]

df_filtered = df[df["Country"].isin(selected_countries)]

df_grouped = df_filtered.groupby(["Year", "Country"]).sum().reset_index()

df_grouped["Total"] = df_grouped[
    ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"]
].astype(float).sum(axis=1).astype(int)

df_grouped = df_grouped.iloc[:-1]

country_totals = df_grouped.groupby("Country")["Total"].sum().reset_index()
country_totals = country_totals.sort_values(by="Total", ascending=False)

from IPython.display import display
display(country_totals.head())


# %%
# 3. Organizing time series with pivot tables and Melt

pivot_df = df_grouped.pivot(index="Year", columns="Country", values=df_grouped.columns[2:]).fillna(0)
print(pivot_df)

df_melted = df_grouped.melt(id_vars=["Country", "Year"], 
                            var_name="Month", 
                            value_name="Value")

df_melted["Date"] = df_melted["Year"].astype(str) + "-" + df_melted["Month"].str[:3]
df_melted = df_melted.drop(columns=["Year", "Month"])

display(df_melted.head())


# %%
import pandas as pd

df_melted['Date_dt'] = pd.to_datetime(df_melted['Date'], format='%Y-%b', errors='coerce')

df_melted = df_melted.dropna(subset=['Date_dt'])

df_melted = df_melted.sort_values(by='Date_dt')

df_melted = df_melted.drop(columns='Date_dt')

# %%
# 4. Loading and preprocessing exchange rate data (KRW to USD)

url = "https://raw.githubusercontent.com/seung-m1nsong/Data698/refs/heads/main/EXKOUS%20(1).csv"
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


# %%
# 5. Loading and preprocessing exchange rate data (Euro to USD)

url = "https://raw.githubusercontent.com/seung-m1nsong/Data698/refs/heads/main/DEXUSEU%20(1).csv"
df_euro = pd.read_csv(url)

print(df_euro.columns)

df_euro = df_euro.iloc[:, :2]  
df_euro.columns = ["Date", "Close"]  

df_euro.rename(columns={"Close": "euro_rate"}, inplace=True)
df_euro["Date"] = pd.to_datetime(df_euro["Date"])
df_euro["Year-Month"] = df_euro["Date"].dt.strftime("%Y-%b")
df_euro = df_euro.drop(columns=["Date"])
df_euro.rename(columns={"Year-Month": "Date"}, inplace=True)

df_jap = df_euro[["Date", "euro_rate"]]

display(df_euro.head())

# %%
# 6. Loading and preprocessing exchange rate data (GBP to USD)

url = "https://raw.githubusercontent.com/seung-m1nsong/Data698/refs/heads/main/GBPUSD.csv"
df_GBP = pd.read_csv(url)

print(df_GBP.columns)

df_GBP.rename(columns={"Close": "GBP_rate"}, inplace=True)
df_GBP["Date"] = pd.to_datetime(df_GBP["Date"])
df_GBP["Year-Month"] = df_GBP["Date"].dt.strftime("%Y-%b")
df_GBP = df_GBP.drop(columns=["Date"])
df_GBP.rename(columns={"Year-Month": "Date"}, inplace=True)

display(df_GBP.head())

# %%
# 7. Loading and preprocessing exchange rate data (Jap to USD)

url = "https://raw.githubusercontent.com/seung-m1nsong/Data698/refs/heads/main/EXJPUS.csv"
df_jap = pd.read_csv(url)

df_jap.rename(columns={"observation_date": "Date", "EXJPUS": "Jap_rate"}, inplace=True)
df_jap["Date"] = pd.to_datetime(df_jap["Date"])
df_jap["Year-Month"] = df_jap["Date"].dt.strftime("%Y-%b")
df_jap = df_jap.drop(columns=["Date"])
df_jap.rename(columns={"Year-Month": "Date"}, inplace=True)

df_jap = df_jap[["Date", "Jap_rate"]]

display(df_jap.head())

missing_values = df_jap.isnull().sum()
missing_values = missing_values[missing_values > 0]
print(missing_values)

# %%
# 8. Loading and preprocessing exchange rate data (Aus to USD)

url = "https://raw.githubusercontent.com/seung-m1nsong/Data698/refs/heads/main/AUDUSD.csv"
df_aud = pd.read_csv(url)

print(df_aud.columns)

df_aud.rename(columns={"Close": "aud_rate"}, inplace=True)
df_aud["Date"] = pd.to_datetime(df_GBP["Date"])
df_aud["Year-Month"] = df_aud["Date"].dt.strftime("%Y-%b")
df_aud = df_aud.drop(columns=["Date"])
df_aud.rename(columns={"Year-Month": "Date"}, inplace=True)

display(df_aud.head())

# %%
# 9. Oil price (WTI crude oil price) data preprocessing

url = "https://raw.githubusercontent.com/seung-m1nsong/Data698/refs/heads/main/Crude%20Oil%20WTI%20Futures%20Historical%20Data.csv"
df_oil = pd.read_csv(url)

df_oil = df_oil.drop(columns=["Open", "High", "Low", "Vol.", "Change %"])

df_oil["Date"] = pd.to_datetime(df_oil["Date"]).dt.strftime("%Y-%b")
df_oil["Date"] = pd.to_datetime(df_oil["Date"], format="%Y-%b")
df_oil = df_oil.sort_values(by="Date", ascending=True) 
df_oil["Date"] = df_oil["Date"].dt.strftime("%Y-%b")

display(df_oil.head())

# %%
# 10. Energy Consumption Data Refinement and Processing

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


# %%
# 11. Merge Data Frames Kor

#display(df_melted.head())
#display(df_kor.head())
#display(df_energy.head())
#display(df_oil.head())

df_korea = df_melted[df_melted['Country'] == 'South Korea']

df_merged_kor = pd.merge(df_korea, df_kor, on='Date', how='left')

df_merged_kor = pd.merge(df_merged_kor, df_energy, on='Date', how='left')

df_merged_kor = pd.merge(df_merged_kor, df_oil, on='Date', how='left')

df_merged_kor.rename(columns={
    'Total': 'Energy_Total',
    'Price': 'Oil_Price'
}, inplace=True)

display(df_merged_kor.head())


# %%
# 12. Merge DataFrames UK

df_UK = df_melted[df_melted['Country'] == 'United Kingdom']

df_merged_UK = pd.merge(df_UK, df_GBP, on='Date', how='left')

df_merged_UK = pd.merge(df_merged_UK, df_energy, on='Date', how='left')

df_merged_UK = pd.merge(df_merged_UK, df_oil, on='Date', how='left')

df_merged_UK.rename(columns={
    'Total': 'Energy_Total',
    'Price': 'Oil_Price'
}, inplace=True)

display(df_merged_UK.head())

# %%
# 13. Merge DataFrames Jap

df_Japan = df_melted[df_melted['Country'] == 'Japan']

df_merged_Jap = pd.merge(df_Japan, df_jap, on='Date', how='left')

df_merged_Jap = pd.merge(df_merged_Jap, df_energy, on='Date', how='left')

df_merged_Jap = pd.merge(df_merged_Jap, df_oil, on='Date', how='left')

df_merged_Jap.rename(columns={
    'Total': 'Energy_Total',
    'Price': 'Oil_Price'
}, inplace=True)

display(df_merged_Jap.head())

# %%
# 14. Merge DataFrames France

df_france = df_melted[df_melted['Country'] == 'France']

df_merged_Fr = pd.merge(df_france, df_euro, on='Date', how='left')

df_merged_Fr = pd.merge(df_merged_Fr, df_energy, on='Date', how='left')

df_merged_Fr = pd.merge(df_merged_Fr, df_oil, on='Date', how='left')

df_merged_Fr.rename(columns={
    'Total': 'Energy_Total',
    'Price': 'Oil_Price'
}, inplace=True)

display(df_merged_Fr.head())

# %%
# 15. Merge DataFrames Australia

df_australia = df_melted[df_melted['Country'] == 'Australia']

df_merged_aud = pd.merge(df_australia, df_aud, on='Date', how='left')

df_merged_aud = pd.merge(df_merged_aud, df_energy, on='Date', how='left')

df_merged_aud = pd.merge(df_merged_aud, df_oil, on='Date', how='left')

df_merged_aud.rename(columns={
    'Total': 'Energy_Total',
    'Price': 'Oil_Price'
}, inplace=True)

display(df_merged_aud.head())

# %%
# 16. Stationarity Test and Differencing of Time Series Data (ADF Test & Differencing)

exog_columns = ['Kor_rate', 'Energy_Total', 'Oil_Price']

for col in exog_columns:
    df_merged_kor[col] = pd.to_numeric(df_merged_kor[col], errors='coerce')

exog_columns = ['Jap_rate', 'Energy_Total', 'Oil_Price']

for col in exog_columns:
    df_merged_Jap[col] = pd.to_numeric(df_merged_Jap[col], errors='coerce')
    
exog_columns = ['GBP_rate', 'Energy_Total', 'Oil_Price']

for col in exog_columns:
    df_merged_UK[col] = pd.to_numeric(df_merged_UK[col], errors='coerce')
    
exog_columns = ['euro_rate', 'Energy_Total', 'Oil_Price']

for col in exog_columns:
    df_merged_Fr[col] = pd.to_numeric(df_merged_Fr[col], errors='coerce')
    
exog_columns = ['aud_rate', 'Energy_Total', 'Oil_Price']

for col in exog_columns:
    df_merged_aud[col] = pd.to_numeric(df_merged_aud[col], errors='coerce')

# %%
from statsmodels.tsa.stattools import adfuller

def adf_test(series, col_name=''):
    result = adfuller(series.dropna())
    print(f"✅ ADF Test for: {col_name}")
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    print("Critical Values:")
    for key, value in result[4].items():
        print(f"   {key}: {value}")
    print("↓ Result ↓")
    if result[1] < 0.05:
        print("✅ Stationary (p < 0.05)")
    else:
        print("❌ Non-stationary (p >= 0.05)")

# %%
columns_to_test = ['Kor_rate', 'Energy_Total', 'Oil_Price']

for col in columns_to_test:
    print(f"\n=== 🔍 ADF Test for: {col} ===")
    series = df_merged_kor[col].dropna()

    adf_test(series, col_name=f'{col} (original)')

    diff_1 = series.diff().dropna()
    adf_test(diff_1, col_name=f'{col} (1st diff)')
    
    if col == 'Energy_Total':
        diff_2 = diff_1.diff().dropna()
        adf_test(diff_2, col_name=f'{col} (2nd diff)')
    
columns_to_test = ['Jap_rate', 'Energy_Total', 'Oil_Price']

for col in columns_to_test:
    print(f"\n=== 🔍 ADF Test for: {col} ===")
    series = df_merged_Jap[col].dropna()

    adf_test(series, col_name=f'{col} (original)')

    diff_1 = series.diff().dropna()
    adf_test(diff_1, col_name=f'{col} (1st diff)')
    
    if col == 'Energy_Total':
        diff_2 = diff_1.diff().dropna()
        adf_test(diff_2, col_name=f'{col} (2nd diff)')

columns_to_test = ['euro_rate', 'Energy_Total', 'Oil_Price']

for col in columns_to_test:
    print(f"\n=== 🔍 ADF Test for: {col} ===")
    series = df_merged_Fr[col].dropna()

    adf_test(series, col_name=f'{col} (original)')

    diff_1 = series.diff().dropna()
    adf_test(diff_1, col_name=f'{col} (1st diff)')
    
    if col == 'Energy_Total':
        diff_2 = diff_1.diff().dropna()
        adf_test(diff_2, col_name=f'{col} (2nd diff)')
    
columns_to_test = ['GBP_rate', 'Energy_Total', 'Oil_Price']

for col in columns_to_test:
    print(f"\n=== 🔍 ADF Test for: {col} ===")
    series = df_merged_UK[col].dropna()

    adf_test(series, col_name=f'{col} (original)')

    diff_1 = series.diff().dropna()
    adf_test(diff_1, col_name=f'{col} (1st diff)')
    
    if col == 'Energy_Total':
        diff_2 = diff_1.diff().dropna()
        adf_test(diff_2, col_name=f'{col} (2nd diff)')
    
columns_to_test = ['aud_rate', 'Energy_Total', 'Oil_Price']

for col in columns_to_test:
    print(f"\n=== 🔍 ADF Test for: {col} ===")
    series = df_merged_aud[col].dropna()

    adf_test(series, col_name=f'{col} (original)')

    diff_1 = series.diff().dropna()
    adf_test(diff_1, col_name=f'{col} (1st diff)')

    if col == 'Energy_Total':
        diff_2 = diff_1.diff().dropna()
        adf_test(diff_2, col_name=f'{col} (2nd diff)')


# %%
# 17. Construction of First and Second Differences for Stationarity

columns_to_diff = ['Kor_rate', 'Energy_Total', 'Oil_Price']

for col in columns_to_diff:
    df_merged_kor[f'{col}_diff'] = df_merged_kor[col].diff()

df_merged_kor['Energy_Total_diff2'] = df_merged_kor['Energy_Total_diff'].diff()
    
display(df_merged_kor.head())

columns_to_diff = ['Jap_rate', 'Energy_Total', 'Oil_Price']

for col in columns_to_diff:
    df_merged_Jap[f'{col}_diff'] = df_merged_Jap[col].diff()

df_merged_Jap['Energy_Total_diff2'] = df_merged_Jap['Energy_Total_diff'].diff()
    
display(df_merged_Jap.head())

columns_to_diff = ['euro_rate', 'Energy_Total', 'Oil_Price']

for col in columns_to_diff:
    df_merged_Fr[f'{col}_diff'] = df_merged_Fr[col].diff()

df_merged_Fr['Energy_Total_diff2'] = df_merged_Fr['Energy_Total_diff'].diff()
    
display(df_merged_Fr.head())

columns_to_diff = ['GBP_rate', 'Energy_Total', 'Oil_Price']

for col in columns_to_diff:
    df_merged_UK[f'{col}_diff'] = df_merged_UK[col].diff()

df_merged_UK['Energy_Total_diff2'] = df_merged_UK['Energy_Total_diff'].diff()
    
display(df_merged_UK.head())

columns_to_diff = ['aud_rate', 'Energy_Total', 'Oil_Price']

for col in columns_to_diff:
    df_merged_aud[f'{col}_diff'] = df_merged_aud[col].diff()
    
df_merged_aud['Energy_Total_diff2'] = df_merged_aud['Energy_Total_diff'].diff()
    
display(df_merged_aud.head())

# %%
# 18. Import volume comparison

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from highlight_text import ax_text

df_filtered = df_melted[df_melted['Date'] != '2024-Dec']

countries = df_filtered['Country'].unique()

cmap = get_cmap("tab20", len(countries))
colors = [cmap(i) for i in range(len(countries))]

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

for i, country in enumerate(countries):
        df_country = df_filtered[df_filtered['Country'] == country]
        ax.plot(df_country['Date'], df_country['Value'], label=country, color=colors[i], linewidth=1)
        ax.text(df_country['Date'].iloc[-1], df_country['Value'].iloc[-1],
                country, fontsize=8, fontweight='bold', color=colors[i],
                va='center', ha='left')

ax.set_title("U.S. Imports by Country (2015–2024, excluding Dec 2024)", fontsize=12)
ax.set_ylabel("Import Value")
ax.set_xlabel("Date")

ax.grid(False)
ax.set_facecolor("white")
ax.spines[["top", "right"]].set_visible(False)
plt.xticks(rotation=90, fontsize=6)

plt.tight_layout()
plt.show()

# %%
# 19. Time Series Diagnostics for Import Value (Korea)

import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.graphics.tsaplots as sgt
import statsmodels.tsa.stattools as sts
from statsmodels.tsa.seasonal import seasonal_decompose

ts = df_merged_kor['Value'].diff().dropna()

decomposition = seasonal_decompose(ts, model='additive', period=1)
fig = decomposition.plot()
fig.set_size_inches(5, 5)
plt.show()

# 2. ACF & PACF
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

sgt.plot_acf(ts, lags=15, zero=False, ax=ax1)
ax1.set_title("Korea Rate ACF of Value_diff")

sgt.plot_pacf(ts, lags=15, zero=False, method='ols', ax=ax2)
ax2.set_title("Korea Rate PACF of Value_diff")

fig.set_size_inches(3, 3)
plt.tight_layout()
plt.show()

# 3. ADF Test
adf_result = sts.adfuller(ts)
print(f"ADF Statistic: {adf_result[0]}")
print(f"p-value: {adf_result[1]}")


# %%
# 20. ADF Stationarity Test for Exogenous Variables

import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.graphics.tsaplots as sgt
import statsmodels.tsa.stattools as sts
from statsmodels.tsa.seasonal import seasonal_decompose

for col in ['Kor_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']:
    ts_exog = df_merged_kor[col].dropna()
    result = sts.adfuller(ts_exog)
    print(f"\n=== ADF Test for {col} ===")
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    
for col in ['Jap_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']:
    ts_exog = df_merged_Jap[col].dropna()
    result = sts.adfuller(ts_exog)
    print(f"\n=== ADF Test for {col} ===")
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    
for col in ['GBP_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']:
    ts_exog = df_merged_UK[col].dropna()
    result = sts.adfuller(ts_exog)
    print(f"\n=== ADF Test for {col} ===")
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    
for col in ['euro_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']:
    ts_exog = df_merged_Fr[col].dropna()
    result = sts.adfuller(ts_exog)
    print(f"\n=== ADF Test for {col} ===")
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    
for col in ['aud_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']:
    ts_exog = df_merged_aud[col].dropna()
    result = sts.adfuller(ts_exog)
    print(f"\n=== ADF Test for {col} ===")
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")

# %%
# 21. ARIMAX Estimation with Korean Exogenous Variables

from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

cols = ['Value', 'Kor_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']
df_model = df_merged_kor[cols].dropna()

y = df_model['Value']

exog = df_merged_kor[['Kor_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']].dropna()

min_len = min(len(y), len(exog))
y = y[-min_len:]
exog = exog[-min_len:]

model = SARIMAX(endog=y, exog=exog, order=(1,0,1), enforce_stationarity=True, enforce_invertibility=True)
result = model.fit(disp=False)

print(result.summary())


# %%
# 22. Arimax + robust Kor

from statsmodels.tsa.statespace.sarimax import SARIMAX

cols = ['Value', 'Kor_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']
df_model = df_merged_kor[cols].dropna()

y = df_model['Value']

exog = df_model[['Kor_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']]  

model = SARIMAX(endog=y, exog=exog, order=(1, 0, 1),
                enforce_stationarity=True, enforce_invertibility=True)
result_robust = model.fit(disp=False, cov_type='robust')

print(result_robust.summary())


# %%
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

cols = ['Value', 'Jap_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']
df_model = df_merged_Jap[cols].dropna()

y = df_model['Value']

exog = df_merged_Jap[['Jap_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']].dropna()

min_len = min(len(y), len(exog))
y = y[-min_len:]
exog = exog[-min_len:]

model = SARIMAX(endog=y, exog=exog, order=(1, 0, 1), enforce_stationarity=True, enforce_invertibility=True)
result = model.fit(disp=False)

print(result.summary())



# %% [markdown]
# ✅ Arimax + robust 

# %%
# 23 Arimax + robust Jap

from statsmodels.tsa.statespace.sarimax import SARIMAX

# 필요한 컬럼만 추출
cols = ['Value', 'Jap_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']
df_model = df_merged_Jap[cols].dropna()

# 종속 변수
y = df_model['Value']

# 외생 변수
exog = df_model[['Jap_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']]  # 여기 수정됨

# SARIMAX + robust 표준오차
model = SARIMAX(endog=y, exog=exog, order=(1, 0, 1),
                enforce_stationarity=True, enforce_invertibility=True)
result_robust = model.fit(disp=False, cov_type='robust')

# 결과 출력
print(result_robust.summary())


# %%
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

cols = ['Value', 'GBP_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']
df_model = df_merged_UK[cols].dropna()

y = df_model['Value']

exog = df_merged_UK[['GBP_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']].dropna()

min_len = min(len(y), len(exog))
y = y[-min_len:]
exog = exog[-min_len:]

model = SARIMAX(endog=y, exog=exog, order=(1, 0, 1), enforce_stationarity=True, enforce_invertibility=True)
result = model.fit(disp=False)

print(result.summary())


# %%
# 23. Arimax + robust GBP

from statsmodels.tsa.statespace.sarimax import SARIMAX

cols = ['Value', 'GBP_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']
df_model = df_merged_UK[cols].dropna()

y = df_model['Value']

exog = df_model[['GBP_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']]  

model = SARIMAX(endog=y, exog=exog, order=(1, 0, 1),
                enforce_stationarity=True, enforce_invertibility=True)
result_robust = model.fit(disp=False, cov_type='robust')

print(result_robust.summary())


# %%
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

cols = ['Value', 'euro_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']
df_model = df_merged_Fr[cols].dropna()

y = df_model['Value']

exog = df_merged_Fr[['euro_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']].dropna()

min_len = min(len(y), len(exog))
y = y[-min_len:]
exog = exog[-min_len:]

model = SARIMAX(endog=y, exog=exog, order=(1, 0, 1), enforce_stationarity=True, enforce_invertibility=True)
result = model.fit(disp=False)

print(result.summary())

# %%
# 24. Arimax + robust Jap

from statsmodels.tsa.statespace.sarimax import SARIMAX

cols = ['Value', 'euro_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']
df_model = df_merged_Fr[cols].dropna()

y = df_model['Value']

exog = df_model[['euro_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']]  

# SARIMAX + robust SD
model = SARIMAX(endog=y, exog=exog, order=(1, 0, 1),
                enforce_stationarity=True, enforce_invertibility=True)
result_robust = model.fit(disp=False, cov_type='robust')

print(result_robust.summary())

# %%
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

cols = ['Value', 'aud_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']
df_model = df_merged_aud[cols].dropna()

y = df_model['Value']

exog = df_merged_aud[['aud_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']].dropna()

min_len = min(len(y), len(exog))
y = y[-min_len:]
exog = exog[-min_len:]

model = SARIMAX(endog=y, exog=exog, order=(1, 0, 1), enforce_stationarity=True, enforce_invertibility=True)
result = model.fit(disp=False)

print(result.summary())

# %%
# 25. Arimax + robust Jap

from statsmodels.tsa.statespace.sarimax import SARIMAX

cols = ['Value', 'aud_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']
df_model = df_merged_aud[cols].dropna()

y = df_model['Value']

exog = df_model[['aud_rate_diff', 'Energy_Total_diff2', 'Oil_Price_diff']] 

model = SARIMAX(endog=y, exog=exog, order=(1, 0, 1),
                enforce_stationarity=True, enforce_invertibility=True)
result_robust = model.fit(disp=False, cov_type='robust')

print(result_robust.summary())

# %%
model = SARIMAX(endog=y, exog=exog, order=(1,0,1), 
                enforce_stationarity=True, enforce_invertibility=True)
result = model.fit(disp=False)

residuals = result.resid

# %%
from arch import arch_model

garch_model = arch_model(residuals, vol='GARCH', p=1, q=1)
garch_result = garch_model.fit(disp='off')

print(garch_result.summary())

# %%
# 26. Find Elasticity

import pandas as pd

coefficients = {
    "Kor_rate_diff": 286300,
    "Jap_rate_diff": 639800,
    "euro_rate_diff": -139500000,
    "GBP_rate_diff": -57980000,
    "aud_rate_diff": -6960000,
    "Energy_Total_diff2": 722700, 
    "Oil_Price_diff": 135000       
}

avg_import_value = 1.5e8 
change_percent = {
    "Kor_rate_diff": 0.01,    
    "Jap_rate_diff": 0.01,
    "euro_rate_diff": 0.01,
    "GBP_rate_diff": 0.01,
    "aud_rate_diff": 0.01,
    "Energy_Total_diff2": 0.01,  
    "Oil_Price_diff": 0.01       
}

sensitivity = {
    var: (coeff / avg_import_value) / change_percent[var]
    for var, coeff in coefficients.items()
}

sensitivity_df = pd.DataFrame({
    "Variable": list(sensitivity.keys()),
    "Coefficient": [coefficients[k] for k in sensitivity.keys()],
    "Avg_Import_Value": avg_import_value,
    "Assumed % Change in Variable": [change_percent[k] * 100 for k in sensitivity.keys()],
    "Estimated % Change in Import": [round((coefficients[k] / avg_import_value) * 100, 2) for k in sensitivity.keys()],
    "Elasticity (Sensitivity)": [round(v, 2) for v in sensitivity.values()]
})

display(sensitivity_df)