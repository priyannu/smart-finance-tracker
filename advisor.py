import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def advisor(user_input, metrics, history):
    system_prompt = f"""You are a smart personal finance advisor. 
The user's current financial data is:
- Income: ₹{metrics['income']:.2f}
- Spending: ₹{metrics['spending']:.2f}
- Balance: ₹{metrics['balance']:.2f}
- Savings Rate: {metrics['savings_rate']:.2f}%

Give short, practical, friendly advice based on this data. 
Always respond in 2-3 sentences max. Use ₹ for currency."""

    # Limit input size to prevent abuse
    user_input = user_input[:500]

    messages = [{"role": "system", "content": system_prompt}]

    for role, msg in history[-6:]:
        messages.append({
            "role": "user" if role == "User" else "assistant",
            "content": msg[:500]
        })

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=messages,
        max_tokens=200,
        timeout=10
    )

    return response.choices[0].message.content
