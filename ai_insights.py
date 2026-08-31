def generate_insights(df):
    insights = []

    total = df["amount"].sum()
    if total > 0:
        insights.append("💰 You are saving money overall.")
    else:
        insights.append("⚠️ You are overspending.")

    top_category = df.groupby("category")["amount"].sum().idxmin()
    insights.append(f"📉 Highest spending in: {top_category}")

    avg_expense = df[df["amount"] < 0]["amount"].mean()
    insights.append(f"📊 Avg expense: ₹{abs(avg_expense):.0f}")

    return insights