from pyhive import hive
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = hive.Connection(host='localhost', port=10000, username='root', auth='NONE')
print("Connected to Hive successfully!")

# --- RFM segment summary ---
query_rfm = """
SELECT
    rfm_segment,
    COUNT(*) AS num_customers,
    ROUND(AVG(recency_days), 1) AS avg_recency_days,
    ROUND(AVG(frequency), 1) AS avg_frequency,
    ROUND(SUM(monetary), 2) AS total_revenue
FROM rfm_segments
GROUP BY rfm_segment
ORDER BY total_revenue DESC
"""
rfm_summary = pd.read_sql(query_rfm, conn)
print("\nRFM Segments:\n", rfm_summary)

# --- Monthly revenue trend ---
query_trend = """
SELECT
    SUBSTR(InvoiceDate, 1, 7) AS year_month,
    ROUND(SUM(Quantity * Price), 2) AS monthly_revenue,
    COUNT(DISTINCT Invoice) AS num_orders
FROM retail_clean
GROUP BY SUBSTR(InvoiceDate, 1, 7)
ORDER BY year_month
"""
monthly_trend = pd.read_sql(query_trend, conn)
print("\nMonthly Trend:\n", monthly_trend)

conn.close()
print("\nGenerating new charts...")

sns.set_style("whitegrid")

# --- Chart: RFM segment revenue ---
plt.figure(figsize=(10, 6))
order = rfm_summary.sort_values('total_revenue', ascending=True)
colors = sns.color_palette("viridis", len(order))
plt.barh(order['rfm_segment'], order['total_revenue'], color=colors)
plt.title('Total Revenue by RFM Customer Segment', fontsize=14, fontweight='bold')
plt.xlabel('Total Revenue (£)')
plt.ylabel('Segment')
for i, (val, cnt) in enumerate(zip(order['total_revenue'], order['num_customers'])):
    plt.text(val, i, f"  {cnt} customers", va='center', fontsize=9)
plt.tight_layout()
plt.savefig('rfm_segments.png', dpi=150)
print("Saved: rfm_segments.png")

# --- Chart: Monthly revenue trend ---
plt.figure(figsize=(12, 6))
plt.plot(monthly_trend['year_month'], monthly_trend['monthly_revenue'], marker='o', color='#2E86AB', linewidth=2)
plt.title('Monthly Revenue Trend (Dec 2009 - Dec 2011)', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Revenue (£)')
plt.xticks(rotation=45, ha='right')
plt.axvspan('2010-10', '2010-11', color='gold', alpha=0.15)
plt.axvspan('2011-09', '2011-11', color='gold', alpha=0.15)
plt.tight_layout()
plt.savefig('monthly_trend.png', dpi=150)
print("Saved: monthly_trend.png")

print("\nDone.")