import streamlit as st
import pandas as pd
from categorizer import categorize
from charts import generate_charts
from analytics import compute_metrics
from advisor import advisor
from report import generate_report
from auth import create_db, login, register
from ai_insights import generate_insights

create_db()

st.set_page_config(layout="wide")
st.title("💰 Finance AI Pro MAX")

# ---------------- LOGIN SYSTEM ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if not st.session_state.logged_in:

    if choice == "Login":
        st.subheader("🔐 Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
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

        if st.button("Register"):
            if not new_user or not new_pass:
                st.error("Username and password cannot be empty")
            elif len(new_pass) < 6:
                st.error("Password must be at least 6 characters")
            else:
                msg = register(new_user, new_pass)
                if "exists" in msg:
                    st.error(msg)
                else:
                    st.success(msg)

# ---------------- MAIN APP ----------------
else:
    st.sidebar.success("Logged in")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.chat_history = []
        st.rerun()

    page = st.sidebar.selectbox(
        "Navigate",
        ["Dashboard", "AI Insights", "Advisor"]
    )

    uploaded = st.file_uploader("Upload your transaction CSV", type=["csv"])

    if uploaded:
        try:
            df = pd.read_csv(uploaded)

            if not all(col in df.columns for col in ["date", "description", "amount"]):
                st.error("CSV must contain: date, description, amount")

            else:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                df["category"] = df["description"].apply(categorize)

                # ---------------- DATE FILTER ----------------
                st.sidebar.divider()
                st.sidebar.subheader("📅 Date Filter")
                min_date = df["date"].min().date()
                max_date = df["date"].max().date()

                start_date = st.sidebar.date_input("From", value=min_date, min_value=min_date, max_value=max_date)
                end_date = st.sidebar.date_input("To", value=max_date, min_value=min_date, max_value=max_date)

                df = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]

                if df.empty:
                    st.warning("No transactions found in the selected date range.")
                    st.stop()

                # METRICS
                metrics = compute_metrics(df)

                # ---------------- SPENDING ALERTS ----------------
                if metrics["income"] > 0:
                    spend_pct = (metrics["spending"] / metrics["income"]) * 100
                    if spend_pct >= 90:
                        st.error(f"🔴 You've spent {spend_pct:.0f}% of your income. Immediate action needed!")
                    elif spend_pct >= 70:
                        st.warning(f"⚠️ You've spent {spend_pct:.0f}% of your income this period.")

                if metrics["savings_rate"] < 10:
                    st.warning("⚠️ Your savings rate is below 10%. Try to cut down on expenses.")

                top_category = df[df["amount"] < 0].groupby("category")["amount"].sum().idxmin()
                top_amount = abs(df[df["amount"] < 0].groupby("category")["amount"].sum().min())
                if top_amount > metrics["income"] * 0.3:
                    st.warning(f"⚠️ High spending in **{top_category}**: ₹{top_amount:.0f} is over 30% of your income.")

                # ---------------- PAGES ----------------
                if page == "Dashboard":

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("💸 Spending", f"₹{metrics['spending']:.2f}")
                    col2.metric("💰 Income", f"₹{metrics['income']:.2f}")
                    col3.metric("🏦 Balance", f"₹{metrics['balance']:.2f}")
                    col4.metric("📈 Savings Rate", f"{metrics['savings_rate']:.2f}%")

                    st.divider()

                    charts = generate_charts(df)
                    for chart in charts:
                        st.plotly_chart(chart, use_container_width=True)

                    st.divider()

                    st.download_button(
                        "📥 Download Processed Data",
                        generate_report(df),
                        file_name="finance_report.csv"
                    )

                elif page == "AI Insights":
                    st.subheader("🤖 Smart AI Insights")
                    insights = generate_insights(df)
                    for i in insights:
                        st.info(i)

                elif page == "Advisor":
                    st.subheader("🤖 AI Financial Advisor (Powered by Llama 3)")

                    if "chat_history" not in st.session_state:
                        st.session_state.chat_history = []

                    user_input = st.text_input("Ask anything about your finances")

                    if st.button("Send"):
                        if user_input.strip():
                            with st.spinner("Thinking..."):
                                try:
                                    response = advisor(user_input, metrics, st.session_state.chat_history)
                                    st.session_state.chat_history.append(("User", user_input))
                                    st.session_state.chat_history.append(("AI", response))
                                except Exception as e:
                                    st.error(f"Advisor error: {e}")

                    for role, msg in st.session_state.chat_history:
                        if role == "User":
                            st.markdown(f"🧑 **You:** {msg}")
                        else:
                            st.markdown(f"🤖 **AI:** {msg}")

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.warning("Upload a CSV file")
