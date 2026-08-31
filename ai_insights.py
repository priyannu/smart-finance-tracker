def generate_insights(df):
    insights = []

    total = df["amount"].sum()
    if total > 0:
        insights.append(f"💰 You are saving money overall. Net balance: ₹{total:.0f}")
    else:
        insights.append(f"⚠️ You are overspending. Net balance: ₹{total:.0f}")

    expenses = df[df["amount"] < 0]
    income = df[df["amount"] > 0]

    if not expenses.empty:
        top_category = expenses.groupby("category")["amount"].sum().idxmin()
        top_amount = abs(expenses.groupby("category")["amount"].sum().min())
        insights.append(f"📉 Highest spending category: **{top_category}** — ₹{top_amount:.0f}")

        avg_expense = abs(expenses["amount"].mean())
        insights.append(f"📊 Average expense per transaction: ₹{avg_expense:.0f}")

        num_transactions = len(expenses)
        insights.append(f"🔢 Total expense transactions: {num_transactions}")

    if not income.empty:
        total_income = income["amount"].sum()
        total_spending = abs(expenses["amount"].sum()) if not expenses.empty else 0
        savings_rate = ((total_income - total_spending) / total_income * 100) if total_income else 0

        if savings_rate >= 20:
            insights.append(f"✅ Great savings rate of {savings_rate:.1f}%! You're meeting the 20% savings goal.")
        elif savings_rate >= 10:
            insights.append(f"🟡 Savings rate is {savings_rate:.1f}%. Try to reach 20% for financial stability.")
        else:
            insights.append(f"🔴 Low savings rate of {savings_rate:.1f}%. Consider reducing discretionary spending.")

    category_counts = df[df["amount"] < 0]["category"].value_counts()
    if not category_counts.empty:
        most_frequent = category_counts.index[0]
        insights.append(f"🛒 Most frequent spending category: **{most_frequent}** ({category_counts.iloc[0]} transactions)")

    return insights
