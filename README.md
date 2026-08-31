# 💰 Finance AI Pro MAX

> A personal finance dashboard built with **Streamlit** — upload your bank transactions, visualize spending, get AI-powered insights and chat with a real LLM-powered financial advisor using RAG, LangGraph, and Chain of Thought reasoning.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)
![Plotly](https://img.shields.io/badge/Plotly-5.x-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Groq](https://img.shields.io/badge/AI-Groq%20LLM-orange)
![LangGraph](https://img.shields.io/badge/Agent-LangGraph-purple)
![RAG](https://img.shields.io/badge/RAG-ChromaDB-blue)

---

## 📌 What is this?

Finance AI Pro MAX is a local web app that helps you understand your personal finances. Upload a simple CSV of your bank transactions and the app automatically:

- Categorizes every transaction (Food, Transport, Shopping, Healthcare, etc.)
- Shows your income, spending, balance, and savings rate
- Renders 4 interactive charts in a 2x2 grid
- Fires smart spending alerts when you overspend
- Gives you 6 detailed AI insights about your spending habits
- Lets you chat with a **real LLM advisor** powered by:
  - 🔵 **RAG** — retrieves your actual transactions from ChromaDB before answering
  - 🟣 **LangGraph** — multi-node agent graph for structured reasoning
  - 🟡 **Chain of Thought** — step-by-step reasoning for accurate answers
- Lets you filter transactions by date range

---

## 🧠 Gen AI Architecture

```
User Question
      ↓
  RAG (ChromaDB)
  Retrieves top 5 relevant transactions
      ↓
  LangGraph Agent
  ┌─────────────────────────────────┐
  │  Node 1: understand_node        │  → Identifies the financial topic
  │  Node 2: cot_node               │  → Chain of Thought reasoning
  │  Node 3: validate_node          │  → Validates the response
  └─────────────────────────────────┘
      ↓
  Groq LLM (Qwen model)
  Generates final answer with context
      ↓
  Response shown to user
```

### 🔵 RAG (Retrieval Augmented Generation)
- All transactions are stored in **ChromaDB** (vector database)
- When you ask a question, the top 5 most relevant transactions are retrieved
- The LLM answers based on your **actual transaction data**, not just summary numbers

### 🟣 LangGraph
- A 3-node agent graph built with LangGraph:
  - `understand_node` — identifies what financial topic the question is about
  - `cot_node` — performs Chain of Thought reasoning and generates the answer
  - `validate_node` — ensures the response is valid before showing it

### 🟡 Chain of Thought (CoT)
- The LLM is prompted to think step by step:
  - Step 1 — What does the financial data tell us?
  - Step 2 — What do the relevant transactions show?
  - Step 3 — What is the best advice?
- Produces more accurate, reasoned answers instead of guessing

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip
- A free [Groq API key](https://console.groq.com)

### 1. Clone the repository
```bash
git clone https://github.com/priyannu/smart-finance-tracker.git
cd smart-finance-tracker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
SCRYPT_SALT=your_custom_salt_here
```
Get a free Groq API key at → https://console.groq.com/keys

### 4. Run the app
```bash
streamlit run app.py
```

### 5. Open in browser
```
http://localhost:8501
```

---

## 📖 How to Use

### Step 1 — Register
- On the sidebar, select **Register**
- Enter a username and password (min 6 characters)
- Click **Register**

### Step 2 — Login
- Switch to **Login** on the sidebar
- Enter your credentials
- Click **Login**

### Step 3 — Upload your CSV
- Click **Browse files** and upload your transaction CSV
- Or use the included `sample_data.csv` to try it out instantly

### Step 4 — Filter by Date (optional)
- Use the **📅 Date Filter** in the sidebar to narrow down transactions

### Step 5 — Explore the pages

#### 📊 Dashboard
- View 4 key metrics: Spending, Income, Balance, Savings Rate
- Automatic spending alerts if you overspend
- 4 interactive charts in a 2x2 grid:
  - Pie chart — spending by category
  - Bar chart — category comparison
  - Line chart — cash flow over time
  - Box plot — spending distribution
- Download your processed data as CSV

#### 🤖 AI Insights
- 6 automatically generated insights:
  - Overall saving or overspending status
  - Highest spending category + amount
  - Average expense per transaction
  - Total number of expense transactions
  - Savings rate with rating (Great / OK / Low)
  - Most frequent spending category

#### 💬 Advisor (LangGraph + RAG + CoT)
- Powered by **Groq + LangGraph + ChromaDB**
- Retrieves your actual transactions before answering
- Thinks step by step using Chain of Thought
- Has memory of last 6 messages
- Example questions:
  - `What is my balance?`
  - `Am I overspending?`
  - `Should I invest?`
  - `Give me budget advice`
  - `How can I save more money?`
  - `Can I afford a big purchase?`

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
smart-finance-tracker/
├── app.py                   # Main Streamlit UI
├── auth.py                  # Login, Register, Logout (SQLite + scrypt hashing)
├── categorizer.py           # Auto-categorizes transactions by keyword
├── analytics.py             # Computes income, spending, balance, savings rate
├── charts.py                # Generates 4 Plotly charts
├── ai_insights.py           # AI spending insights (6 data points)
├── advisor.py               # LangGraph agent with CoT (3-node graph)
├── rag.py                   # RAG module — ChromaDB vector store
├── report.py                # CSV export
├── agent.py                 # CLI version of the advisor
├── sample_data.csv          # Sample transactions for testing
├── requirements.txt         # Dependencies
└── .streamlit/
    └── config.toml          # Dark theme configuration
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Data Processing | Pandas |
| Charts | Plotly Express |
| Database | SQLite (built-in Python) |
| Vector Database | ChromaDB |
| Password Security | scrypt (built-in hashlib) |
| LLM | Groq API (Qwen model) |
| Agent Framework | LangGraph |
| LLM Orchestration | LangChain |
| Environment Variables | python-dotenv |
| Language | Python 3.8+ |

---

## 🔐 Security

- Passwords hashed using **scrypt** (memory-hard, brute-force resistant)
- Salt stored in `.env` — never hardcoded
- API key stored in `.env` — never in source code
- `users.db` and `.env` excluded from repo via `.gitignore`
- User input sanitized to prevent XSS attacks
- SQL queries use parameterized statements to prevent SQL injection
- LLM input capped at 500 characters to prevent abuse
- Groq API calls have a 10 second timeout

---

## 🏷️ Transaction Categories

| Category | Keywords Detected |
|---|---|
| Food | swiggy, zomato, food, restaurant, cafe, dominos |
| Transport | uber, ola, rapido, metro, petrol, fuel |
| Shopping | amazon, flipkart, myntra, meesho, ajio, nykaa |
| Housing | rent, maintenance, society |
| Bills | electricity, recharge, wifi, broadband, gas, insurance |
| Healthcare | pharmacy, hospital, apollo, medplus, doctor |
| Entertainment | netflix, spotify, prime, hotstar, bookmyshow |
| Education | udemy, coursera, books, course, fees, tuition |
| Income | salary, bonus, credit, refund, cashback |
| Other | anything not matched above |

---

## ⚠️ Known Limitations

- Categorization is keyword-based — custom merchants may fall under "Other"
- Designed for INR (₹) transactions
- Groq free tier has rate limits
- ChromaDB is in-memory — resets on app restart

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
