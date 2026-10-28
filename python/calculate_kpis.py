from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "categorized_transactions.csv"
)

OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "monthly_summary.csv"


df = pd.read_csv(INPUT_PATH, parse_dates=["date"])

# Identify the year and month of each transaction
df["month"] = df["date"].dt.to_period("M").astype(str)

# Separate income from spending
df["income"] = df["amount"].clip(lower=0)
df["spending"] = -df["amount"].clip(upper=0)

# Add up income and spending for each month
monthly_summary = (
    df.groupby("month", as_index=False)[["income", "spending"]]
    .sum()
)

monthly_summary["net_cash_flow"] = (
    monthly_summary["income"] - monthly_summary["spending"]
)

# Leaving the rate undefined when monthly income is zero
monthly_summary["savings_rate_%"] =(
    monthly_summary["net_cash_flow"]
    / monthly_summary["income"].replace(0, float("nan"))
    * 100
)
monthly_summary = monthly_summary.sort_values("month").reset_index(drop=True)

monthly_summary["spending_3m_average"] = (
    monthly_summary["spending"]
    .rolling(window=3, min_periods=3)
    .mean()
)

monthly_summary = monthly_summary.round(2)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

monthly_summary.to_csv(OUTPUT_PATH, index=False)

print("\nMonthly summary:")
print(monthly_summary.to_string(index=False))

print(f"\nMonths in summary: {len(monthly_summary)}")
print(f"Saved monthly summary to: {OUTPUT_PATH}") 