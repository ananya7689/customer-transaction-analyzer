import pandas as pd

sheet1 = pd.read_excel("online_retail_II.xlsx", sheet_name="Year 2009-2010")
sheet2 = pd.read_excel("online_retail_II.xlsx", sheet_name="Year 2010-2011")

combined = pd.concat([sheet1, sheet2], ignore_index=True)
combined.to_csv("online_retail.csv", index=False)

print(f"Done! Combined file has {len(combined)} rows.")