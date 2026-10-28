from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "synthetic_transactions.csv"

START_DATE = "2026-10-01"
N_MONTHS = 12

MONTHLY_SALARY = 2450.00
MONTHLY_RENT = 850.00
MONTHLY_ELECTRICITY = 55.00
MONTHLY_INTERNET = 30.00
MONTHLY_NETFLIX = 13.49
MONTHLY_SPOTIFY = 9.99

rng = np.random.default_rng(seed=42)

GROCERY_MERCHANTS = ["Carrefour Market", "Lidl", "Monoprix", "Auchun"]
RESTAURANT_MERCHANTS = ["Cafe Central", "Restaurant Le Petit", "Deliveroo", "Uber" ]

months = pd.date_range(
    start=START_DATE,
    periods=N_MONTHS,
    freq="MS",
)

transactions = []

for month_start in months:
    transactions.append(
        
        {
            "date": month_start,
            "description": "Monthly salary",
            "amount": MONTHLY_SALARY,
        }
    )

    transactions.append(
        {
            "date": month_start + pd.Timedelta(days=1),
            "description": "Apartment rent",
            "amount": -MONTHLY_RENT,
        }
    )
    recurring_bills = [
        ("Electricity bill", MONTHLY_ELECTRICITY, 4),
        ("Internet bill", MONTHLY_INTERNET, 6),
        ("Netflix subscription", MONTHLY_NETFLIX, 9),
        ("Spotify subscription", MONTHLY_SPOTIFY, 9),
    ]

    for description, amount, day_offset in recurring_bills:
        transactions.append(
            {
                "date": month_start + pd.Timedelta(days=day_offset),
                "description": description,
                "amount": -amount,
            }
        )
        # Generate between 6 and 10 grocery transactions this month
    n_groceries = int(rng.integers(6, 11))

    for _ in range(n_groceries):
        day_offset = int(rng.integers(0, month_start.days_in_month))

        transactions.append(
            {
                "date": month_start + pd.Timedelta(days=day_offset),
                "description": str(rng.choice(GROCERY_MERCHANTS)),
                "amount": -round(float(rng.uniform(15, 80)), 2),
            }
        )

    # Generate between 3 and 7 restaurant transactions this month
    n_restaurants = int(rng.integers(3, 8))

    for _ in range(n_restaurants):
        day_offset = int(rng.integers(0, month_start.days_in_month))

        transactions.append(
            {
                "date": month_start + pd.Timedelta(days=day_offset),
                "description": str(rng.choice(RESTAURANT_MERCHANTS)),
                "amount": -round(float(rng.uniform(8, 50)), 2),
            }
        )


df = pd.DataFrame(transactions)

df = df.sort_values("date").reset_index(drop=True)

df.insert(
    0,
    "transaction_id",
    [f"TXN_{i + 1:05d}" for i in range(len(df))],
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

'''print(df.head(6))
print(f"\nTotal transactions: {len(df)}")
print(f"Saved file to: {OUTPUT_PATH}")

print("\n--- Data checks ---")

print("\nMissing values per column:")
print(df.isna().sum())

print("\nTransaction IDs are unique:")
print(df["transaction_id"].is_unique)

print("\nIncome transactions:")
print((df["amount"] > 0).sum())

print("\nExpense transactions:")
print((df["amount"] < 0).sum())

print("\nDate range:")
print(df["date"].min())
print(df["date"].max())
'''