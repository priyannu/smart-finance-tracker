def categorize(text):
    t = str(text).lower()

    mapping = {
        "Transport": ["uber", "ola", "rapido", "metro", "bus", "petrol", "fuel"],
        "Food": ["swiggy", "zomato", "food", "restaurant", "cafe", "starbucks", "dominos", "mcdonalds"],
        "Shopping": ["amazon", "flipkart", "myntra", "meesho", "ajio", "nykaa", "shopping"],
        "Income": ["salary", "bonus", "credit", "refund", "cashback"],
        "Housing": ["rent", "maintenance", "society"],
        "Bills": ["electricity", "recharge", "wifi", "broadband", "water", "gas", "insurance"],
        "Healthcare": ["pharmacy", "hospital", "apollo", "medplus", "doctor", "clinic", "medicine"],
        "Entertainment": ["netflix", "spotify", "prime", "hotstar", "bookmyshow", "cinema", "youtube"],
        "Education": ["udemy", "coursera", "books", "course", "fees", "tuition"],
    }

    for category, keywords in mapping.items():
        if any(k in t for k in keywords):
            return category

    return "Other"
