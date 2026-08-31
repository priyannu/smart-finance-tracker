def compute_metrics(df):
    total_spent = abs(df[df["amount"] < 0]["amount"].sum())
    total_income = df[df["amount"] > 0]["amount"].sum()
    balance = df["amount"].sum()

    savings_rate = (balance / total_income * 100) if total_income else 0

    return {
        "spending": total_spent,
        "income": total_income,
        "balance": balance,
        "savings_rate": savings_rate
    }