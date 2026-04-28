import pandas as pd
import duckdb
print("Setup working perfectly")
file_path = r"D:\Flagship Projects\agentic_ai_project\Data\Raw\OnlineRetail.csv"
df = pd.read_csv(file_path, encoding="ISO-8859-1")
print(df.head())
print("columns:", df.columns)
print(df.shape)
print(df.info())
print(df.describe())
print(df.isnull().sum())