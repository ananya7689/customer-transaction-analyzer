from pyhive import hive
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to Hive running in Docker
conn = hive.Connection(host='localhost', port=10000, username='root', auth='NONE')
print("Connected to Hive successfully!")

# --- Query 1: Top 10 high-value customers ---
query1 = """
SELECT 
    CustomerID,
    ROUND(SUM(Quantity * Price), 2) AS total_spend,
    COUNT(DISTINCT Invoice) AS num_orders
FROM retail_clean
GROUP BY CustomerID
ORDER BY total_spend DESC
LIMIT 10
"""
top_customers = pd.read_sql(query1, conn)
print("\nTop 10 Customers:\n", top_customers)

# --- Query 2: Top 10 products ---
query2 = """
SELECT 
    Description,
    COUNT(*) AS times_purchased,
    SUM(Quantity) AS total_units_sold
FROM retail_clean
GROUP BY Description
ORDER BY times_purchased DESC
LIMIT 10
"""
top_products = pd.read_sql(query2, conn)
print("\nTop 10 Products:\n", top_products)

# --- Query 3: Customer value tiers ---
query3 = """
SELECT
    value_tier,
    COUNT(*) AS num_customers,
    ROUND(SUM(total_spend), 2) AS tier_total_spend
FROM (
    SELECT
        CustomerID,
        SUM(Quantity * Price) AS total_spend,
        CASE
            WHEN PERCENT_RANK() OVER (ORDER BY SUM(Quantity * Price) DESC) <= 0.1 THEN 'High Value (Top 10%)'
            WHEN PERCENT_RANK() OVER (ORDER BY SUM(Quantity * Price) DESC) <= 0.5 THEN 'Medium Value'
            ELSE 'Low Value'
        END AS value_tier
    FROM retail_clean
    GROUP BY CustomerID
) ranked
GROUP BY value_tier
ORDER BY tier_total_spend DESC
"""
value_tiers = pd.read_sql(query3, conn)
print("\nValue Tiers:\n", value_tiers)

conn.close()
print("\nAll data pulled. Generating charts...")

# --- Set style ---
sns.set_style("whitegrid")

# --- Chart 1: Top 10 customers by spend ---
plt.figure(figsize=(10, 6))
sns.barplot(data=top_customers, x='total_spend', y='customerid', hue='customerid', 
            palette='Blues_d', orient='h', legend=False)
plt.title('Top 10 Customers by Total Spend', fontsize=14, fontweight='bold')
plt.xlabel('Total Spend (£)')
plt.ylabel('Customer ID')
plt.tight_layout()
plt.savefig('top_customers.png', dpi=150)
print("Saved: top_customers.png")

# --- Chart 2: Top 10 products by purchase frequency ---
plt.figure(figsize=(10, 6))
sns.barplot(data=top_products, x='times_purchased', y='description', hue='description',
            palette='Greens_d', orient='h', legend=False)
plt.title('Top 10 Most Frequently Purchased Products', fontsize=14, fontweight='bold')
plt.xlabel('Times Purchased')
plt.ylabel('Product')
plt.tight_layout()
plt.savefig('top_products.png', dpi=150)
print("Saved: top_products.png")

# --- Chart 3: Customer value tier breakdown ---
plt.figure(figsize=(8, 6))
colors = ['#2E86AB', '#A8DADC', '#F1FAEE']
plt.pie(value_tiers['tier_total_spend'], labels=value_tiers['value_tier'], 
        autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Revenue Share by Customer Value Tier', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('value_tiers.png', dpi=150)
print("Saved: value_tiers.png")

print("\nAll charts saved in C:\\hadoop-hive-project\\")