import pandas as pd
##load clean data
df= pd.read_csv(r"D:\Flagship Projects\agentic_ai_project\Data\processed\OnlineRetailClean.csv")
print(df.head())
print(df.shape)
print(df.info())
print(df.describe())
print(df.isnull().sum())
## Fix column names
df.columns = df.columns.str.replace('ï»¿', '').str.strip()
print(df.columns)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], dayfirst=True, errors="coerce")
print(df.dtypes)

## Customers Table
customers = df.groupby("CustomerID").agg({
    "Country": "first"
}).reset_index()
customers.columns = ["customer_id", "country"]
customers["customer_id"] = customers["customer_id"].astype(int)
print(customers.head())
print(customers.shape)

##  Orders Table

orders = df.groupby("InvoiceNo").agg({
    "CustomerID": "first",
    "InvoiceDate": "first"
}).reset_index()
orders.columns = ["order_id", "customer_id", "order_date"]
orders["customer_id"] = orders["customer_id"].astype(int)
print(orders.head())
print(orders.shape)

## Products Table
products = df[["StockCode", "Description"]].drop_duplicates()
products.columns = ["product_id", "product_name"]
print(products.head())
print(products.shape)   

## Order Items Table (FACT)
order_items = df[["InvoiceNo", "StockCode", "Quantity", "UnitPrice"]]
order_items.columns = ["order_id", "product_id", "quantity", "price"]
print(order_items.head())
print(order_items.shape)  

# Save Tables to Files
customers.to_csv(r"D:\Flagship Projects\agentic_ai_project\Data\processed\customers.csv", index=False)
orders.to_csv(r"D:\Flagship Projects\agentic_ai_project\Data\processed\orders.csv", index=False)
products.to_csv(r"D:\Flagship Projects\agentic_ai_project\Data\processed\products.csv", index=False)
order_items.to_csv(r"D:\Flagship Projects\agentic_ai_project\Data\processed\order_items.csv", index=False)
print("Tables saved")
