# Customer Intelligence & Sales Analytics

## Overview

This project presents an end-to-end data analytics solution using retail transaction data. It combines data cleaning, SQL-based analysis, customer segmentation, machine learning, and dashboard visualization to generate actionable business insights.

## Objectives

* Transform raw transactional data into structured analytical datasets
* Analyze sales performance and customer behavior
* Segment customers using RFM (Recency, Frequency, Monetary)
* Predict customer churn using machine learning
* Build an interactive dashboard for decision-making

---

## Tech Stack

* **Python** (Pandas, Scikit-learn)
* **SQL** (DuckDB)
* **Power BI**
* **Machine Learning** (Random Forest)

---

## Project Workflow

### 1. Data Cleaning

* Removed missing Customer IDs
* Filtered invalid records (negative quantity/price)
* Removed duplicates
* Standardized date formats


### 2. Data Modeling

* Created structured tables:

  * Customers
  * Orders
  * Products
  * Order Items


### 3. SQL Analysis

* Revenue calculation
* Monthly sales trends
* Top customers and products
* Country-wise revenue analysis
* Running totals and ranking

### 4. RFM Segmentation

* Calculated:

  * Recency
  * Frequency
  * Monetary
* Segmented customers into value-based groups

### 5. Churn Prediction

* Built Random Forest model
* Predicted churn based on RFM features
* Identified at-risk customers

## Dashboard Features

* KPI metrics (Revenue, Orders, Customers, AOV, Growth)
* Revenue trends over time
* Top products and countries
* Customer segmentation (RFM)
* Order status analysis


## Key Insights

* High-value customers contribute majority of revenue
* Certain countries dominate sales performance
* Sales show seasonal trends
* Customer segmentation helps target retention strategies

## Dashboard Preview

<img width="1414" height="785" alt="image" src="https://github.com/user-attachments/assets/479a3b26-62f6-41d7-812c-31b7a4245349" />

<img width="1460" height="807" alt="image" src="https://github.com/user-attachments/assets/e49ffe6b-ece5-4045-8b49-9d93fcd5c832" />



## Outcome

This project demonstrates how data analytics and machine learning can be integrated to drive business insights and improve customer decision-making.


