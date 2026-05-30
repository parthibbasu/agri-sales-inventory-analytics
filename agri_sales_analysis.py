"""
Agri Retail Sales & Inventory Analytics
Author: Parthib Basu

Run:
python notebooks/agri_sales_analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "agri_sales_inventory_sample.csv"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "assets"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH, parse_dates=["date"])

df["revenue"] = df["units_sold"] * df["unit_price"]
df["cost"] = df["units_sold"] * df["cost_per_unit"]
df["gross_profit"] = df["revenue"] - df["cost"]
df["profit_margin_pct"] = (df["gross_profit"] / df["revenue"] * 100).round(2)
df["stockout_risk"] = df["inventory_units"] < df["units_sold"]

summary = {
    "total_revenue": round(df["revenue"].sum(), 2),
    "total_gross_profit": round(df["gross_profit"].sum(), 2),
    "avg_profit_margin_pct": round(df["profit_margin_pct"].mean(), 2),
    "mismatch_rate_pct": round(df["order_mismatch"].mean() * 100, 2),
    "stockout_risk_rate_pct": round(df["stockout_risk"].mean() * 100, 2),
}

print("Executive KPI Summary")
for key, value in summary.items():
    print(f"{key}: {value}")

category_summary = (
    df.groupby("category")
    .agg(revenue=("revenue", "sum"), gross_profit=("gross_profit", "sum"), units_sold=("units_sold", "sum"))
    .sort_values("revenue", ascending=False)
)

region_summary = (
    df.groupby(["state", "district"])
    .agg(revenue=("revenue", "sum"), mismatch_rate=("order_mismatch", "mean"), stockout_risk=("stockout_risk", "mean"))
    .sort_values("revenue", ascending=False)
)

print("\nCategory Performance")
print(category_summary)

print("\nRegional Performance")
print(region_summary)

category_summary["revenue"].plot(kind="bar", title="Revenue by Category")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "revenue_by_category.png")
plt.close()

monthly = df.groupby(df["date"].dt.to_period("M"))["revenue"].sum()
monthly.index = monthly.index.astype(str)
monthly.plot(kind="line", marker="o", title="Monthly Revenue Trend")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_revenue_trend.png")
plt.close()
