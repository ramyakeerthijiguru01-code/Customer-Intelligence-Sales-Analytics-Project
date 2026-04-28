import pandas as pd
import duckdb

# Load tables
customers = pd.read_csv(r"D:\Flagship Projects\agentic_ai_project\Data\processed\customers.csv")
orders = pd.read_csv(r"D:\Flagship Projects\agentic_ai_project\Data\processed\orders.csv")
products = pd.read_csv(r"D:\Flagship Projects\agentic_ai_project\Data\processed\products.csv")
order_items = pd.read_csv(r"D:\Flagship Projects\agentic_ai_project\Data\processed\order_items.csv")
print("\nTables loaded\n")

# Connect DuckDB
con = duckdb.connect()
print("\nDuckDB connected\n")

# Register tables
con.register("customers", customers)
con.register("orders", orders)
con.register("order_items", order_items)
con.register("products", products)
print("\nTables registered\n")

#Revenue Calculation
result = con.execute("""
SELECT (quantity * price) AS revenue
FROM order_items
""").fetchdf()

print("Total Revenue:")
print(result)


# Monthly Revenue
result = con.execute("""
SELECT strftime(CAST(o.order_date AS TIMESTAMP), '%Y-%m') AS month,
       SUM(oi.quantity * oi.price) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month
""").fetchdf()  

print("\nMonthly Revenue:")
print(result)

## Top 10 Customers
top_customers = con.execute("""
select o.customer_id,
   sum(oi.quantity * oi.price) as revenue
from orders o
join order_items oi on o.order_id = oi.order_id
group by o.customer_id
order by revenue desc
limit 10
""").fetchdf()

print("\nTop 10 Customers:")
print(top_customers)

## Top 10 Products
top_products = con.execute("""
select product_id,
   sum(quantity) as total_quantity
from order_items
group by product_id
order by total_quantity desc
limit 10
""").fetchdf()

print("\nTop 10 Products:")
print(top_products)

## Country Revenue

country_revenue = con.execute("""
select c.country,
   sum(oi.quantity * oi.price) as revenue
from customers c
join orders o 
    on c.customer_id = o.customer_id
join order_items oi 
   on o.order_id = oi.order_id
group by c.country
order by revenue desc
""").fetchdf()

print("\nCountry Revenue:")
print(country_revenue)


T_c_with_rank = con.execute("""
 select
    o.customer_id,
    sum(oi.quantity * oi.price) as total_spent,
    rank() over (order by sum(oi.quantity * oi.price) desc) as rank
    
from orders o
join order_items oi 
    on o.order_id = oi.order_id
group by o.customer_id
""").fetchdf()

print("\ntop customers with rank:")
print(T_c_with_rank)

t_p_per_country = con.execute("""
SELECT *
FROM (
    SELECT 
        c.country,
        oi.product_id,
        SUM(oi.quantity) AS total_qty,
        RANK() OVER (
            PARTITION BY c.country 
            ORDER BY SUM(oi.quantity) DESC
        ) AS rank
    FROM customers c
    JOIN orders o 
        ON c.customer_id = o.customer_id
    JOIN order_items oi 
        ON o.order_id = oi.order_id
    GROUP BY c.country, oi.product_id
) t
WHERE rank <= 3
""").fetchdf()

print("\nTOP PRODUCTS PER COUNTRY:\n")
print(t_p_per_country)


## Running Total

running_total = con.execute("""
SELECT 
    strftime(CAST(o.order_date AS TIMESTAMP), '%Y-%m') AS month,
    SUM(oi.quantity * oi.price) AS revenue,
    SUM(SUM(oi.quantity * oi.price)) 
        OVER (ORDER BY strftime(CAST(o.order_date AS TIMESTAMP), '%Y-%m')) 
        AS running_total
FROM orders o
JOIN order_items oi 
    ON o.order_id = oi.order_id
GROUP BY month
""").fetchdf()

print("\nRunning Total:\n")
print(running_total)

## Customer Retention

customer_retention = con.execute("""
SELECT 
    customer_id,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY customer_id
HAVING total_orders > 1
""").fetchdf()

print("\nCustomer Retention:\n")
print(customer_retention)

## Customer Churn

churn_data = con.execute("""
SELECT 
    customer_id,
    MAX(order_date) AS last_purchase
FROM orders
GROUP BY customer_id
""").fetchdf()

## MAX(order_date) → last time customer bought
print("\nchurn_data:\n")
print(churn_data.head())

## Identify churned customers
## Today = latest date in dataset
## Churn if inactive for 90 days

churn_analysis = con.execute("""
SELECT 
    customer_id,
    MAX(order_date) AS last_purchase,
    CASE 
        WHEN DATE_DIFF('day', CAST(MAX(order_date) AS TIMESTAMP), CURRENT_DATE) > 90 
        THEN 'Churned'
        ELSE 'Active'
    END AS status
FROM orders
GROUP BY customer_id
""").fetchdf()
## Converts string → proper date format sql - CAST(MAX(order_date) AS TIMESTAMP)
## fo this CAST(... AS TIMESTAMP)
print("\nchurn_analysis:\n")
print(churn_analysis.head())


## Churn Rate

churn_rate = con.execute("""
SELECT 
    COUNT(CASE WHEN status = 'Churned' THEN 1 END) * 100.0 / COUNT(*) AS churn_rate
FROM (
    SELECT 
        customer_id,
        CASE 
            WHEN DATE_DIFF('day', CAST(MAX(order_date) AS TIMESTAMP), CURRENT_DATE) > 90 
            THEN 'Churned'
            ELSE 'Active'
        END AS status
    FROM orders
    GROUP BY customer_id
) t
""").fetchdf()

print("\nChurn Rate:")
print(churn_rate)

### RFM Recency, Frequency, monetory

rfm = con.execute("""
SELECT 
    o.customer_id,

    DATE_DIFF('day', 
        CAST(MAX(o.order_date) AS TIMESTAMP), 
        CURRENT_DATE
    ) AS recency,

    COUNT(DISTINCT o.order_id) AS frequency,

    SUM(oi.quantity * oi.price) AS monetary

FROM orders o
JOIN order_items oi 
    ON o.order_id = oi.order_id

GROUP BY o.customer_id
""").fetchdf()

print("\nRFM:\n")
print(rfm.head())

## Save rfm

rfm.to_csv(r"D:\Flagship Projects\agentic_ai_project\Data\processed\rfm.csv", index=False)
print("\nRFM saved")