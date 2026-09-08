# Customer Transaction Analyzer

A big data analytics pipeline that processes 1M+ retail transactions using **Hadoop (HDFS)** for distributed storage, **Hive** for SQL-style aggregation at scale, and **Python** for analysis and visualization — built to identify high-value customers and purchasing patterns for a retail business.

## Key Insight

The top 10% of customers by spend (588 people) generate **63.7% of total revenue** — a clear Pareto pattern with direct implications for retention strategy.

RFM segmentation further reveals an **"At Risk"** segment of 829 historically frequent customers who haven't purchased in 365+ days, representing £1.6M in recoverable value — a stronger win-back target than the broader churned base.

## Architecture
CSV Dataset → HDFS Storage → Hive External Table → HiveQL Aggregation → Python (PyHive + pandas) → Visualizations

## Tech Stack

- **Storage:** Hadoop HDFS (Docker, `bde2020` images)
- **Query engine:** Apache Hive 2.3.2, Hive Metastore on PostgreSQL
- **Analysis:** Python 3.12, PyHive, pandas, Matplotlib, Seaborn
- **Environment:** Docker Desktop (WSL2 backend), single-node local sandbox

## What This Project Does

1. Ingests 1,067,371 raw retail transactions (UCI "Online Retail II" dataset) into HDFS
2. Creates a Hive external table over the raw data
3. Cleans data down to 794,389 valid transactions (removes returns, cancellations, guest checkouts, invalid pricing)
4. Runs HiveQL aggregations for:
   - Total spend & order frequency per customer
   - Top purchased products
   - Customer value tier segmentation (spend-based)
   - **RFM segmentation** (Recency, Frequency, Monetary) into 6 behavioral segments
   - Monthly revenue trend / seasonality analysis
5. Connects Python to Hive via PyHive to pull results into pandas
6. Generates 5 visualizations (bar charts, pie chart, line chart)

## Files in This Repo

| File | Purpose |
|---|---|
| `docker-compose.yml` | Defines the Hadoop + Hive multi-container cluster |
| `hadoop-hive.env` | Environment config for HDFS and Hive |
| `analyze_retail.py` | Connects to Hive, pulls top customers/products, generates initial charts |
| `analyze_retail_v2.py` | Adds RFM segmentation and monthly trend analysis |
| `*.png` | Generated chart outputs |

## Sample Results

**RFM Segments:**

| Segment | Customers | Avg Recency (days) | Avg Frequency | Total Revenue (£) |
|---|---|---|---|---|
| Champions | 1,311 | 19.2 | 16.9 | 12,033,482 |
| Loyal Customers | 1,385 | 69.1 | 5.5 | 2,681,122 |
| At Risk | 829 | 365.7 | 4.9 | 1,618,072 |
| Lost/Churned | 1,521 | 460.0 | 1.3 | 654,972 |

## How to Run

1. `docker-compose up -d` — starts Hadoop (namenode, datanode) and Hive (metastore + server)
2. Load the CSV into HDFS: `hdfs dfs -put your_data.csv /retail_data/`
3. Create the Hive external table (see HiveQL in project report)
4. `pip install pandas matplotlib seaborn pyhive thrift thrift-sasl`
5. `python analyze_retail_v2.py`

## Author

Ananya Kumari — Big Data Analytics project, September 2026
