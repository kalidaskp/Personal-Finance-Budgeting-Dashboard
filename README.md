# Personal Budgeting Dashboard

A Streamlit dashboard for exploring personal spending, income, savings, and monthly financial trends using synthetic transaction data.

## Features

- Monthly overview of income, expenses, savings, and savings rate
- Category spending breakdown
- Monthly income and expense trends
- Interactive date and category filters
- CSV export for filtered transaction data
- Synthetic data generation for safe, reproducible testing

## Project Structure

```text
.
├── app.py
├── data/
│   └── raw/
│       └── synthetic_transactions.csv
├── scripts/
│   └── generate_synthetic_data.py
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd personal-budgeting-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

- macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run app.py
```

The app should open automatically in your browser.

## Data

This project uses **synthetic transaction data** generated locally. It does not contain real bank information.

The dataset includes transaction dates, descriptions, categories, transaction types, and amounts.

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- NumPy

## Next Steps

- Add budget targets by category
- Add recurring transaction detection
- Add savings-goal tracking
- Improve data validation and error handling