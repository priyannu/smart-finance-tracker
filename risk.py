def compute_risk_scores(df, metrics):
    """
    Computes per-category risk scores and overall financial risk.
    Returns a dict with category scores and overall risk level.
    """
    income = metrics["income"]
    scores = {}

    if income == 0:
        return {"overall": "UNKNOWN", "overall_score": 0, "categories": {}}

    expenses = df[df["amount"] < 0]
    category_totals = expenses.groupby("category")["amount"].sum().abs()

    # Budget thresholds as % of income
    thresholds = {
        "Food":          0.15,
        "Shopping":      0.10,
        "Transport":     0.08,
        "Entertainment": 0.05,
        "Bills":         0.15,
        "Housing":       0.30,
        "Healthcare":    0.10,
        "Education":     0.10,
        "Other":         0.05,
    }

    for category, amount in category_totals.items():
        threshold = thresholds.get(category, 0.10)
        ratio = amount / income
        if ratio >= threshold * 2:
            scores[category] = {"amount": amount, "risk": "🔴 CRITICAL", "score": 100}
        elif ratio >= threshold * 1.5:
            scores[category] = {"amount": amount, "risk": "🟠 HIGH", "score": 75}
        elif ratio >= threshold:
            scores[category] = {"amount": amount, "risk": "🟡 MEDIUM", "score": 50}
        else:
            scores[category] = {"amount": amount, "risk": "🟢 LOW", "score": 25}

    # Overall score
    overall_score = 0
    if metrics["income"] > 0:
        spend_ratio = metrics["spending"] / metrics["income"]
        if spend_ratio >= 0.9:
            overall_score = 90
        elif spend_ratio >= 0.7:
            overall_score = 65
        elif spend_ratio >= 0.5:
            overall_score = 40
        else:
            overall_score = 15

    if metrics["savings_rate"] < 5:
        overall_score = min(overall_score + 20, 100)
    elif metrics["savings_rate"] < 10:
        overall_score = min(overall_score + 10, 100)

    if overall_score >= 75:
        overall = "🔴 CRITICAL"
    elif overall_score >= 50:
        overall = "🟠 HIGH"
    elif overall_score >= 25:
        overall = "🟡 MEDIUM"
    else:
        overall = "🟢 LOW"

    return {
        "overall": overall,
        "overall_score": overall_score,
        "categories": scores
    }
