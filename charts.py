import pandas as pd
import plotly.express as px


def generate_charts(df):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    charts = []

    # Pie chart — only expenses, converted to positive
    expense_df = df[df["amount"] < 0].copy()
    expense_df["amount"] = expense_df["amount"].abs()
    charts.append(px.pie(expense_df, names="category", values="amount", title="Spending by Category"))

    charts.append(px.bar(df, x="category", y="amount", title="Category Comparison"))
    charts.append(px.line(df.sort_values("date"), x="date", y="amount", title="Cash Flow Trend"))
    charts.append(px.box(df, y="amount", title="Spending Distribution"))

    return charts
