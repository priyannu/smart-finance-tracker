class FinancialCoTEngine:
    """
    Financial Chain-of-Thought (F-CoT) Reasoning Engine.
    Structures multi-step financial reasoning before generating a response.
    """

    def __init__(self, metrics: dict, context: str):
        self.income = metrics["income"]
        self.spending = metrics["spending"]
        self.balance = metrics["balance"]
        self.savings_rate = metrics["savings_rate"]
        self.context = context

    def step1_analyze_financials(self) -> str:
        if self.savings_rate >= 30:
            status = "excellent"
        elif self.savings_rate >= 20:
            status = "healthy"
        elif self.savings_rate >= 10:
            status = "moderate"
        else:
            status = "critical"

        return (
            f"Income: ₹{self.income:.0f}, Spending: ₹{self.spending:.0f}, "
            f"Balance: ₹{self.balance:.0f}, Savings Rate: {self.savings_rate:.1f}% ({status})"
        )

    def step2_analyze_transactions(self) -> str:
        if not self.context:
            return "No specific transactions retrieved."
        lines = self.context.strip().split("\n")
        return f"{len(lines)} relevant transactions retrieved: {self.context[:300]}"

    def step3_risk_assessment(self) -> str:
        score = self.compute_risk_score()
        if score >= 75:
            return f"Risk Level: CRITICAL (score {score}/100) — immediate action required"
        elif score >= 50:
            return f"Risk Level: HIGH (score {score}/100) — reduce spending"
        elif score >= 25:
            return f"Risk Level: MEDIUM (score {score}/100) — monitor spending"
        else:
            return f"Risk Level: LOW (score {score}/100) — finances are healthy"

    def compute_risk_score(self) -> int:
        score = 0
        if self.income > 0:
            spend_ratio = self.spending / self.income
            if spend_ratio >= 0.9:
                score += 50
            elif spend_ratio >= 0.7:
                score += 35
            elif spend_ratio >= 0.5:
                score += 20
            else:
                score += 5

        if self.savings_rate < 5:
            score += 30
        elif self.savings_rate < 10:
            score += 20
        elif self.savings_rate < 20:
            score += 10

        if self.balance < 0:
            score += 20

        return min(score, 100)

    def build_prompt(self, question: str) -> str:
        s1 = self.step1_analyze_financials()
        s2 = self.step2_analyze_transactions()
        s3 = self.step3_risk_assessment()

        return f"""You are a personal finance advisor using Financial Chain-of-Thought (F-CoT) reasoning.

=== F-CoT REASONING ENGINE OUTPUT ===
Step 1 - Financial Analysis: {s1}
Step 2 - Transaction Analysis: {s2}
Step 3 - Risk Assessment: {s3}
=====================================

Question: {question}

Based on the F-CoT analysis above, provide a clear, friendly, actionable answer in 2-3 sentences. Use ₹ for currency."""
