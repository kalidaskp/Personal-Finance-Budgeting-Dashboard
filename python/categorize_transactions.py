from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "synthetic_transactions.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "categorized_transactions.csv"


CATEGORY_RULES = {
    "Income": ["salary"],
    "Rent": ["rent"],
    "Groceries": ["carrefour", "lidl", "monoprix", "auchun"],
    "Restaurants": ["cafe", "restaurant", "deliveroo", "uber"],
    "Utilities": ["electricity", "internet"],
    "Subscriptions": ["netflix", "spotify"],
}


def categorize_transaction(description):
    text = str(description).lower()

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in text:
                return category

    return "Uncategorized"


df = pd.read_csv(INPUT_PATH, parse_dates=["date"])

df["category"] = df["description"].apply(categorize_transaction)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

print(df.head(10))

print("\nTransactions per category:")
print(df["category"].value_counts())

print("\nUncategorized transactions:")
print((df["category"] == "Uncategorized").sum())

print(f"\nSaved categorized data to: {OUTPUT_PATH}")