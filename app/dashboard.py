from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "monthly_summary.csv"
TRANSACTIONS_PATH = (PROJECT_ROOT / "data" / "processed" / "categorized_transactions.csv")

MONTHLY_BUDGETS = {
    "Rent": 850.00,
    "Groceries": 400.00,
    "Restaurants": 150.00,
    "Utilities": 90.00,
    "Subscriptions": 30.00,
}

st.set_page_config(
    page_title="Personal Finance Dashboard",
    layout="wide",
)

st.title("Personal Finance & Budgeting Dashboard")

st.caption(
    "Synthetic transaction data covering October 2026 – September 2027. "
    "All amounts are in EUR."
)

if not INPUT_PATH.exists(): 
    st.error("Monthly summary not found. Run calculate_kpis.py first.")
    st.stop()


monthly_summary = pd.read_csv(INPUT_PATH)

month_options = ["All months"] + sorted(
    monthly_summary["month"].unique().tolist()
)

selected_month = st.selectbox(
    "Choose a month",
    options=month_options,
)

if selected_month == "All months":
    filtered_summary = monthly_summary.copy()
else:
    filtered_summary = monthly_summary[
        monthly_summary["month"] == selected_month
    ].copy()
    
total_income = filtered_summary["income"].sum()
total_spending = filtered_summary["spending"].sum()
net_cash_flow = total_income - total_spending


st.subheader(f"Overview: {selected_month}")

col1, col2, col3 = st.columns(3)

col1.metric("Total income (EUR)", round(total_income, 2))
col2.metric("Total spending (EUR)", round(total_spending, 2))
col3.metric("Net cash flow (EUR)", round(net_cash_flow, 2))


st.subheader("Monthly summary")

st.dataframe(
    filtered_summary,
    column_config={
        "savings_rate_pct": "Savings rate percentage"
    },
)
st.subheader("Income and spending over time")

st.caption(
    "This chart always shows all 12 months. "
    "The month filter applies only to the KPI cards and summary table."
)

trend_data = monthly_summary.sort_values("month")

st.line_chart(
    trend_data,
    x="month",
    y=["income", "spending"],
)
st.subheader(f"Spending by category: {selected_month}")

if not TRANSACTIONS_PATH.exists():
    st.error("Categorized transactions not found. Run categorize_transactions.py first.")
    st.stop()

transactions = pd.read_csv(
    TRANSACTIONS_PATH,
    parse_dates=["date"],
)

transactions["month"] = (
    transactions["date"].dt.to_period("M").astype(str)
)

if selected_month == "All months":
    selected_transactions = transactions.copy()
else:
    selected_transactions = transactions[
        transactions["month"] == selected_month
    ].copy()

expenses = selected_transactions[
    selected_transactions["amount"] < 0
].copy()

expenses["spending"] = -expenses["amount"]

category_spending = (
    expenses.groupby("category", as_index=False)["spending"]
    .sum()
    .sort_values("spending", ascending=True)
)

fig = px.bar(
    category_spending,
    x="spending",
    y="category",
    orientation="h",
    labels={
        "spending": "Spending (EUR)",
        "category": "Category",
    },
)

st.plotly_chart(fig, use_container_width=True)
st.subheader(f"Budget versus actual: {selected_month}")

# Match the budget period to the selected spending period
if selected_month == "All months":
    number_of_months = monthly_summary["month"].nunique()
else:
    number_of_months = 1

budget_table = pd.DataFrame(
    list(MONTHLY_BUDGETS.items()),
    columns=["category", "monthly_budget"],
)

budget_table["period_budget"] = (
    budget_table["monthly_budget"] * number_of_months
)

# Attach actual category spending to the budget table
budget_comparison = budget_table.merge(
    category_spending[["category", "spending"]],
    on="category",
    how="left",
)

budget_comparison["spending"] = (
    budget_comparison["spending"].fillna(0)
)

budget_comparison["remaining_budget"] = (
    budget_comparison["period_budget"]
    - budget_comparison["spending"]
)

budget_comparison["status"] = "Within budget"

budget_comparison.loc[
    budget_comparison["remaining_budget"] < 0,
    "status",
] = "Over budget"

st.dataframe(
    budget_comparison[
        [
            "category",
            "period_budget",
            "spending",
            "remaining_budget",
            "status",
        ]
    ].round(2),
    column_config={
        "category": "Category",
        "period_budget": "Budget (EUR)",
        "spending": "Actual spending (EUR)",
        "remaining_budget": "Remaining budget (EUR)",
        "status": "Status",
    },
    hide_index=True,
)
st.subheader("Monthly spending and three-month average")

st.caption(
    "Full-period view. The average includes the current month and "
    "the previous two months. It begins in December 2026."
)

spending_trend = monthly_summary.sort_values("month")

fig_spending_trend = px.line(
    spending_trend,
    x="month",
    y=["spending", "spending_3m_average"],
    markers=True,
    labels={
        "month": "Month",
        "value": "Amount (EUR)",
        "variable": "Measure",
    },
)

st.plotly_chart(fig_spending_trend, use_container_width=True)

st.subheader("Transaction explorer")

st.caption(
    "The month selection above applies here. "
    "The category and search filters below affect only this transaction table."
)

category_options = sorted(
    transactions["category"].dropna().unique().tolist()
)

selected_categories = st.multiselect(
    "Choose transaction categories",
    options=category_options,
    default=category_options,
)

search_text = st.text_input(
    "Search transaction descriptions",
    placeholder="For example: Carrefour, Netflix, or salary",
)

explorer_data = selected_transactions.copy()

explorer_data = explorer_data[
    explorer_data["category"].isin(selected_categories)
]

if search_text.strip():
    explorer_data = explorer_data[
        explorer_data["description"].str.contains(
            search_text.strip(),
            case=False,
            regex=False,
            na=False,
        )
    ]

explorer_data = explorer_data.sort_values(
    ["date", "transaction_id"],
    ascending=[False, True],
)

display_columns = [
    "transaction_id",
    "date",
    "description",
    "amount",
    "category",
]

st.write(f"Matching transactions: {len(explorer_data)}")

st.dataframe(
    explorer_data[display_columns],
    hide_index=True,
    column_config={
        "transaction_id": "Transaction ID",
        "date": st.column_config.DateColumn(
            "Date",
            format="DD/MM/YYYY",
        ),
        "description": "Description",
        "amount": st.column_config.NumberColumn(
            "Amount (EUR)",
            format="%.2f",
        ),
        "category": "Category",
    },
)

if explorer_data.empty:
    st.info("No transactions match your filters.")
    
    st.download_button(
    label="Download matching transactions",
    data=explorer_data[display_columns].to_csv(index=False).encode("utf-8"),
    file_name="filtered_transactions.csv",
    mime="text/csv",
    disabled=explorer_data.empty,
)