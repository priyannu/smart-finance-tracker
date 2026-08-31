def categorize(text):
    t = str(text).lower()

    mapping = {
        "Transport": ["uber", "ola", "rapido"],
        "Food": ["swiggy", "zomato", "food"],
        "Shopping": ["amazon", "flipkart", "myntra"],
        "Income": ["salary", "bonus"],
        "Housing": ["rent"],
        "Bills": ["electricity", "recharge", "wifi"]
    }

    for category, keywords in mapping.items():
        if any(k in t for k in keywords):
            return category

    return "Other"