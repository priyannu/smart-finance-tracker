import streamlit as st
import pandas as pd
from categorizer import categorize
from charts import generate_charts
from analytics import compute_metrics
from advisor import advisor
from report import generate_report
from auth import create_db, login, register
from ai_insights import generate_insights
from rag import build_rag
from risk import compute_risk_scores

create_db()

st.set_page_config(
    page_title="Finance AI Pro MAX",
    page_icon="💰",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    /* Hide default header */
    #MainMenu, footer, header {visibility: hidden;}

    /* App background */
    .stApp { background-color: #0e1117; }

    /* Hero title */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00ff88, #00bfff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .hero-sub {
        color: #888;
        font-size: 1rem;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #1a1f2e;
        border: 1px solid #2a2f3e;
        border-radius: 12px;
        padding: 16px;
    }

    /* Chat bubbles */
    .chat-user {
        background: #1a3a2a;
        border-left: 3px solid #00ff88;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
        color: #e0e0e0;
    }
    .chat-ai {
        background: #1a1f2e;
        border-left: 3px solid #00bfff;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
        color: #e0e0e0;
    }

    /* Insight cards */
    .insight-card {
        background: #1a1f2e;
        border: 1px solid #2a2f3e;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 8px 0;
        font-size: 0.95rem;
        color: #e0e0e0;
    }

    /* Feature cards on landing */
    .feature-card {
        background: #1a1f2e;
        border: 1px solid #00ff8833;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        color: #e0e0e0;
    }

    /* Divider */
    hr { border-color: #2a2f3e; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #12151f;
        border-right: 1px solid #2a2f3e;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00ff88, #00bfff);
        color: #000;
        font-weight: 700;
        border: none;
        border-radius: 8px;
    }
    .stButton > button:hover {
        opacity: 0.85;
        color: #000;
    }

    /* Form submit button */
    .stFormSubmitButton > button {
        background: linear-gradient(90deg, #00ff88, #00bfff);
        color: #000 !important;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN SYSTEM ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if not st.session_state.logged_in:

    # Hero section
    st.markdown('<p class="hero-title">💰 Finance AI Pro MAX</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Your personal AI-powered finance dashboard — RAG · LangGraph · Chain of Thought</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card">📊<br><b>Smart Dashboard</b><br><span style="color:#888;font-size:0.85rem">4 interactive charts + key metrics</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card">🤖<br><b>AI Insights</b><br><span style="color:#888;font-size:0.85rem">6 auto-generated spending insights</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-card">💬<br><b>LLM Advisor</b><br><span style="color:#888;font-size:0.85rem">Groq + LangGraph + RAG chatbot</span></div>', unsafe_allow_html=True)

    st.divider()

    if choice == "Login":
        st.subheader("🔐 Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            if not user or not pwd:
                st.error("Username and password cannot be empty")
            elif login(user, pwd):
                st.session_state.logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    elif choice == "Register":
        st.subheader("📝 Register")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Register", use_container_width=True):
            if not new_user or not new_pass:
                st.error("Username and password cannot be empty")
            elif len(new_pass) < 6:
                st.error("Password must be at least 6 characters")
            else:
                msg = register(new_user, new_pass)
                if "exists" in msg:
                    st.error(msg)
                else:
                    st.success(msg + " — Now login from the sidebar!")

# ---------------- MAIN APP ----------------
else:
    # Sidebar
    st.sidebar.markdown('<p style="color:#00ff88;font-weight:700;font-size:1.1rem">💰 Finance AI Pro MAX</p>', unsafe_allow_html=True)
    st.sidebar.success("✅ Logged in")

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.chat_history = []
        st.rerun()

    st.sidebar.divider()

    page = st.sidebar.selectbox(
        "📂 Navigate",
        ["📊 Dashboard", "🤖 AI Insights", "💬 Advisor"]
    )

    st.sidebar.divider()
    st.sidebar.info("📁 Upload a CSV with columns:\n`date`, `description`, `amount`")

    # Page header
    st.markdown('<p class="hero-title">💰 Finance AI Pro MAX</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Your personal AI-powered finance dashboard</p>', unsafe_allow_html=True)

    uploaded = st.file_uploader("📂 Upload your transaction CSV", type=["csv"])

    if uploaded:
        try:
            df = pd.read_csv(uploaded)

            if not all(col in df.columns for col in ["date", "description", "amount"]):
                st.error("❌ CSV must contain exactly these columns: date, description, amount")

            else:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                df["category"] = df["description"].apply(categorize)

                if "session_id" not in st.session_state:
                    import uuid
                    st.session_state.session_id = str(uuid.uuid4())
                file_name = uploaded.name
                if st.session_state.get("uploaded_file") != file_name:
                    st.session_state.rag_collection = build_rag(df)
                    st.session_state.uploaded_file = file_name
                    st.session_state.chat_history = []

                # ---------------- DATE FILTER ----------------
                st.sidebar.subheader("📅 Date Filter")
                min_date = df["date"].min().date()
                max_date = df["date"].max().date()
                start_date = st.sidebar.date_input("From", value=min_date, min_value=min_date, max_value=max_date)
                end_date = st.sidebar.date_input("To", value=max_date, min_value=min_date, max_value=max_date)

                df = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]

                if df.empty:
                    st.warning("⚠️ No transactions found in the selected date range.")
                    st.stop()

                metrics = compute_metrics(df)

                # ---------------- SPENDING ALERTS ----------------
                if metrics["income"] > 0:
                    spend_pct = (metrics["spending"] / metrics["income"]) * 100
                    if spend_pct >= 90:
                        st.error(f"🔴 Critical: You've spent {spend_pct:.0f}% of your income. Immediate action needed!")
                    elif spend_pct >= 70:
                        st.warning(f"⚠️ You've spent {spend_pct:.0f}% of your income this period.")

                if metrics["savings_rate"] < 10:
                    st.warning("⚠️ Your savings rate is below 10%. Try to cut down on expenses.")

                expenses_by_cat = df[df["amount"] < 0].groupby("category")["amount"].sum()
                if not expenses_by_cat.empty:
                    top_category = expenses_by_cat.idxmin()
                    top_amount = abs(expenses_by_cat.min())
                    if top_amount > metrics["income"] * 0.3:
                        st.warning(f"⚠️ High spending in **{top_category}**: ₹{top_amount:.0f} is over 30% of your income.")

                # ---------------- DASHBOARD ----------------
                if page == "📊 Dashboard":
                    st.subheader("📊 Dashboard")
                    st.divider()

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("💸 Total Spending", f"₹{metrics['spending']:,.0f}")
                    col2.metric("💰 Total Income", f"₹{metrics['income']:,.0f}")
                    col3.metric("🏦 Balance", f"₹{metrics['balance']:,.0f}")
                    col4.metric("📈 Savings Rate", f"{metrics['savings_rate']:.1f}%")

                    # Risk Scores
                    st.divider()
                    risk = compute_risk_scores(df, metrics)
                    st.markdown(f"**🛡️ Overall Financial Risk: {risk['overall']} (Score: {risk['overall_score']}/100)**")
                    if risk["categories"]:
                        rcols = st.columns(len(risk["categories"]))
                        for idx, (cat, data) in enumerate(risk["categories"].items()):
                            rcols[idx].markdown(f"**{cat}**\n\n{data['risk']}\n\n₹{data['amount']:,.0f}")

                    st.divider()

                    charts = generate_charts(df)
                    col_a, col_b = st.columns(2)
                    col_a.plotly_chart(charts[0], use_container_width=True)
                    col_b.plotly_chart(charts[1], use_container_width=True)
                    col_c, col_d = st.columns(2)
                    col_c.plotly_chart(charts[2], use_container_width=True)
                    col_d.plotly_chart(charts[3], use_container_width=True)

                    st.divider()
                    st.download_button(
                        "📥 Download Processed Data as CSV",
                        generate_report(df),
                        file_name="finance_report.csv",
                        use_container_width=True
                    )

                # ---------------- AI INSIGHTS ----------------
                elif page == "🤖 AI Insights":
                    st.subheader("🤖 Smart AI Insights")
                    st.caption("Automatically generated analysis of your transactions")
                    st.divider()

                    insights = generate_insights(df)
                    for insight in insights:
                        st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)

                # ---------------- ADVISOR ----------------
                elif page == "💬 Advisor":
                    st.subheader("💬 AI Financial Advisor")
                    st.caption("Powered by Groq + LangGraph + RAG — Ask anything about your finances")
                    st.divider()

                    # Suggested questions
                    st.markdown("**💡 Try asking:**")
                    cols = st.columns(3)
                    suggestions = [
                        "Am I overspending?",
                        "Should I invest?",
                        "Give me budget advice",
                        "What is my balance?",
                        "How can I save more?",
                        "Can I afford a big purchase?"
                    ]
                    for i, s in enumerate(suggestions):
                        cols[i % 3].markdown(f"`{s}`")

                    st.divider()

                    if "chat_history" not in st.session_state:
                        st.session_state.chat_history = []

                    with st.form("chat_form", clear_on_submit=True):
                        user_input = st.text_input("Ask anything about your finances", placeholder="e.g. Should I invest? Am I overspending?")
                        submitted = st.form_submit_button("Send 💬", use_container_width=True)

                    if submitted and user_input.strip():
                        with st.spinner("🤔 Thinking..."):
                            try:
                                response = advisor(user_input, metrics, st.session_state.chat_history, st.session_state.get("rag_collection"), st.session_state.get("session_id", "default"))
                                st.session_state.chat_history.append(("User", user_input))
                                st.session_state.chat_history.append(("AI", response))
                            except Exception as e:
                                st.error(f"Advisor error: {e}")

                    # Chat history
                    for role, msg in st.session_state.chat_history:
                        if role == "User":
                            st.markdown(f'<div class="chat-user">🧑 <b>You:</b> {msg}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="chat-ai">🤖 <b>AI:</b> {msg}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error reading file: {e}")

    else:
        st.markdown("""
        <div style="background:#1a1f2e;border:1px dashed #2a2f3e;border-radius:12px;padding:30px;text-align:center;color:#888;">
            👆 <b style="color:#e0e0e0">Upload a CSV file above to get started</b><br><br>
            You can use the <code>sample_data.csv</code> included in the repo to try it instantly.
        </div>
        """, unsafe_allow_html=True)
