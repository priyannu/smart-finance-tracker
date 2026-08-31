import html


def handle_memory(user, history):
    if "my name is" in user:
        name = html.escape(user.split("my name is")[-1].strip())
        return f"Nice to meet you, {name}! 😊"

    if "what is my name" in user:
        for role, msg in reversed(history):
            if "my name is" in msg.lower():
                name = html.escape(msg.lower().split("my name is")[-1].strip())
                return f"Your name is {name} 😊"
        return "I don't know your name yet."

    return None


def handle_finance(user, balance, spending, income, savings_rate):
    if "afford" in user:
        if balance > spending:
            return "Yes, you can afford it 👍 but keep savings."
        return "Not recommended based on your finances ⚠️"

    if "save" in user or "saving" in user:
        if savings_rate < 20:
            return f"You should increase savings. Current: {savings_rate:.2f}% (target ≥20%)"
        return f"Good savings rate: {savings_rate:.2f}% 👍"

    if "overspending" in user:
        if spending > income * 0.7:
            return "⚠️ You are overspending. Reduce expenses."
        return "✅ Your spending is under control."

    if "invest" in user:
        if savings_rate < 20:
            return "First improve savings, then invest."
        return "You can invest in SIPs, mutual funds, or index funds."

    if "budget" in user:
        return "Use 50-30-20 rule: Needs 50%, Wants 30%, Savings 20%."

    if "emergency" in user:
        return "Keep 3–6 months of expenses as emergency fund."

    return None


def handle_basic(user, balance, spending, income):
    if "balance" in user:
        return f"Balance: ₹{balance:.2f}"
    if "spending" in user:
        return f"Spending: ₹{spending:.2f}"
    if "income" in user:
        return f"Income: ₹{income:.2f}"
    if "hello" in user or "hi" in user:
        return "Hello! 👋 I'm your financial advisor."
    return None


def advisor(user_input, metrics, history):
    balance = metrics["balance"]
    spending = metrics["spending"]
    income = metrics["income"]
    savings_rate = metrics["savings_rate"]

    user_input = user_input.lower()
    questions = user_input.replace("?", ".").split(".")
    questions = [q.strip() for q in questions if q.strip()]

    responses = []

    for user in questions:
        reply = (
            handle_memory(user, history)
            or handle_finance(user, balance, spending, income, savings_rate)
            or handle_basic(user, balance, spending, income)
            or "I can help with finance questions like savings, budget, investing."
        )
        responses.append(reply)

    return "\n\n".join(responses)
