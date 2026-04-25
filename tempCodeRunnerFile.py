import pandas as pd
import numpy as np

# --- 1. SETUP ---
file_name = "most-popular-programming-languages-2004-2024.csv"
df = pd.read_csv(file_name)

# Assigned Language logic 
student_id_last_3 = 519 
languages = ['C#', 'Flutter', 'Java', 'JavaScript', 'Matlab', 'PhP', 'Python', 'React', 'Swift', 'TypeScript']
languages.sort()
assigned_lang = languages[student_id_last_3 % 10]

# Find the specific column for my assigned language
# This searches for a column that starts with my language name
col = [c for c in df.columns if c.startswith(assigned_lang)][0]

print(f"Analyzing: {assigned_lang} (Column: {col})")

# --- 2. DATA CLEANING & GROWTH ---
df['Month'] = pd.to_datetime(df['Month'])
df_analysis = df[['Month', col]].copy()
df_analysis.rename(columns={col: 'Popularity'}, inplace=True)

# Month-to-month growth rate percentage
df_analysis['Growth_Rate'] = df_analysis['Popularity'].pct_change() * 100

# Rolling statistics (6-month window as per instructions)
df_analysis['Moving_Avg'] = df_analysis['Popularity'].rolling(window=6).mean()
df_analysis['Moving_STD'] = df_analysis['Popularity'].rolling(window=6).std()

# --- 3. LIFECYCLE CLASSIFICATION ---
mean_growth = df_analysis['Growth_Rate'].mean()
std_growth = df_analysis['Growth_Rate'].std()

# Define conditions based on your worksheet rules
conditions = [S
    (df_analysis['Growth_Rate'] > 0) & (df_analysis['Growth_Rate'] < mean_growth),
    (df_analysis['Growth_Rate'] > mean_growth),
    (df_analysis['Growth_Rate'].abs() <= 1),
    (df_analysis['Growth_Rate'] < 0) & (df_analysis['Growth_Rate'] < (-1 * std_growth))
]
choices = ['Introduction', 'Growth', 'Maturity', 'Decline']

df_analysis['Lifecycle_Phase'] = np.select(conditions, choices, default='Maturity')

# --- 4. OUTPUTS ---
print("\n--- Summary Stats ---")
print(df_analysis['Popularity'].describe())

print("\n--- Phase Distribution ---")
print(df_analysis['Lifecycle_Phase'].value_counts())

# Show the final table (first few rows)
print("\n--- Data Preview ---")
print(df_analysis.head(10))