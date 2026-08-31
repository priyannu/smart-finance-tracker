# 💰 Finance AI Pro MAX

> A personal finance dashboard built with **Streamlit** — upload your bank transactions, visualize spending, get AI-powered insights and chatbot advice.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)
![Plotly](https://img.shields.io/badge/Plotly-5.x-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)

---

## 📌 What is this?

Finance AI Pro MAX is a local web app that helps you understand your personal finances. You upload a simple CSV of your bank transactions and the app automatically:

- Categorizes every transaction (Food, Transport, Shopping, etc.)
- Shows your income, spending, balance, and savings rate
- Renders 4 interactive charts
- Gives you smart insights about your spending habits
- Lets you chat with an AI advisor about your finances

---

## 🖥️ Screenshots

| Dashboard | AI Insights | Chatbot Advisor |
|---|---|---|
| Metrics + 4 charts | Spending analysis | Ask finance questions |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/finance-ai-pro.git
cd finance-ai-pro
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Open in browser
```
http://localhost:8501
```

---

## 📖 How to Use

### Step 1 — Register
- On the sidebar, select **Register**
- Enter a username and password
- Click **Register**

### Step 2 — Login
- Switch to **Login** on the sidebar
- Enter your credentials
- Click **Login**

### Step 3 — Upload your CSV
- Click **Browse files** and upload your transaction CSV
- Or use the included `sample_data.csv` to try it out instantly

### Step 4 — Explore the pages

#### 📊 Dashboard
- View 4 key metrics: Spending, Income, Balance, Savings Rate
- Explore 4 interactive charts:
  - Pie chart — spending by category
  - Bar chart — category comparison
  - Line chart — cash flow over time
  - Box plot — spending distribution
- Download your processed data as CSV

#### 🤖 AI Insights
- Automatically generated analysis of your transactions
- Tells you if you're saving or overspending
- Shows your highest spending category and average expense

#### 💬 Advisor (Chatbot)
- Ask questions about your finances in plain English
- Example questions you can ask:
  - `What is my balance?`
  - `Am I overspending?`
  - `Should I invest?`
  - `Give me budget advice`
  - `How are my savings?`
  - `Can I afford a big purchase?`
  - `What is an emergency fund?`

---

## 📂 CSV Format

Your file must have exactly **3 columns**:

| date | description | amount |
|---|---|---|
| 2024-01-01 | Swiggy order | -250 |
| 2024-01-02 | Salary credit | 50000 |
| 2024-01-03 | Amazon purchase | -1200 |

- **Negative amounts** = expenses
- **Positive amounts** = income
- Date format: `YYYY-MM-DD`

A ready-to-use `sample_data.csv` is included in the repo.

---

## 🗂️ Project Structure

```
finance-ai-pro/
├── app.py            # Main Streamlit UI
├── auth.py           # Login, Register, Logout (SQLite + scrypt hashing)
├── categorizer.py    # Auto-categorizes transactions by keyword
├── analytics.py      # Computes income, spending, balance, savings rate
├── charts.py         # Generates 4 Plotly charts
├── ai_insights.py    # Rule-based AI spending insights
├── advisor.py        # Keyword-based chatbot advisor
├── report.py         # CSV export
├── agent.py          # CLI version of the advisor
├── sample_data.csv   # Sample transactions for testing
└── requirements.txt  # Dependencies
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Data Processing | Pandas |
| Charts | Plotly Express |
| Database | SQLite (built-in Python) |
| Password Security | scrypt (built-in hashlib) |
| Language | Python 3.8+ |

---

## 🔐 Security

- Passwords are hashed using **scrypt** (a memory-hard, brute-force resistant algorithm)
- User database (`users.db`) is excluded from the repo via `.gitignore`
- User input is sanitized to prevent XSS attacks
- SQL queries use parameterized statements to prevent SQL injection

---

## 🏷️ Transaction Categories

The app auto-detects these categories from your transaction descriptions:

| Category | Keywords Detected |
|---|---|
| Food | swiggy, zomato, food |
| Transport | uber, ola, rapido |
| Shopping | amazon, flipkart, myntra |
| Housing | rent |
| Bills | electricity, recharge, wifi |
| Income | salary, bonus |
| Other | anything not matched above |

---

## ⚠️ Known Limitations

- Categorization is keyword-based — custom merchants may fall under "Other"
- The chatbot is rule-based, not an LLM
- Designed for INR (₹) transactions

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
