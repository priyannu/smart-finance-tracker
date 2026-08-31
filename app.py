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
            if login(user, pwd):
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
            st.success(register(new_user, new_pass))

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
                df["category"] = df["description"].apply(categorize)

                # METRICS
                metrics = compute_metrics(df)

                if page == "Dashboard":

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("💸 Spending", f"₹{metrics['spending']:.2f}")
                    col2.metric("💰 Income", f"₹{metrics['income']:.2f}")
                    col3.metric("🏦 Balance", f"₹{metrics['balance']:.2f}")
                    col4.metric("📈 Savings Rate", f"{metrics['savings_rate']:.2f}%")

                    st.divider()

                    # CHARTS
                    charts = generate_charts(df)
                    for chart in charts:
                        st.plotly_chart(chart, use_container_width=True)

                    st.divider()

                    # DOWNLOAD
                    st.download_button(
                        "📥 Download Processed Data",
                        generate_report(df),
                        file_name="finance_report.csv"
                    )

                # ---------------- AI INSIGHTS ----------------
                elif page == "AI Insights":
                    st.subheader("🤖 Smart AI Insights")

                    insights = generate_insights(df)
                    for i in insights:
                        st.info(i)

                # ---------------- CHATBOT ----------------
                elif page == "Advisor":

                    st.subheader("🤖 AI Chatbot")

                    if "chat_history" not in st.session_state:
                        st.session_state.chat_history = []

                    user_input = st.text_input("Ask anything about your finances")

                    if st.button("Send"):
                        if user_input:
                            with st.spinner("Thinking..."):
                                response = advisor(user_input, metrics, st.session_state.chat_history)

                                st.session_state.chat_history.append(("User", user_input))
                                st.session_state.chat_history.append(("AI", response))

                    # Display chat nicely
                    for role, msg in st.session_state.chat_history:
                        if role == "User":
                            st.markdown(f"🧑 **You:** {msg}")
                        else:
                            st.markdown(f"🤖 **AI:** {msg}")

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.warning("Upload a CSV file")
