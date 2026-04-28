import pandas as pd
### Load data
filepath = r"D:\Flagship Projects\agentic_ai_project\Data\Raw\OnlineRetail.csv"
df = pd.read_csv(filepath, encoding="ISO-8859-1")
print(df.shape)

## Check Missing Values
print("\nMissing Values\n")
print(df.isnull().sum())

## # Remove Missing CustomerID
df =df.dropna(subset=["CustomerID"])
print("\nAfter removing missing CustomerID:", df.shape)
print(df.isnull().sum())
print("\nMissing Values\n")
print(df.shape)

## Remove Invalid Data

df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]
print("\nAfter removing invalid data:", df.shape)  


##  Remove Duplicates
df = df.drop_duplicates()
print("\nAfter removing duplicates:", df.shape)

## Convert Date Column
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], 
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)## 13-12-2010 → 13 is DAY, not MONTH
print("\nData Types:\n")
print(df.dtypes)

## Save clean data
df.to_csv(r"D:\Flagship Projects\agentic_ai_project\Data\processed\OnlineRetailClean.csv", index=False)
print("\nClean Data Saved")
