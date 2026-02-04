import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SME Financial Health AI", layout="wide")

st.title("📊 SME Financial Health Assessment AI Tool")

uploaded_file = st.file_uploader("Upload Financial CSV", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Financial Data")
    st.dataframe(df)

    # -------- Metrics ----------
    total_revenue = df["revenue"].sum()
    total_expenses = df["expenses"].sum()
    total_profit = total_revenue - total_expenses
    total_loans = df["loan_payment"].sum()
    avg_cash = df["cash_in_bank"].mean()

    profit_margin = (total_profit / total_revenue) * 100
    expense_ratio = (total_expenses / total_revenue) * 100
    debt_ratio = (total_loans / total_revenue) * 100

    # -------- Score ----------
    score = 100
    if profit_margin < 10:
        score -= 25
    if expense_ratio > 80:
        score -= 25
    if debt_ratio > 20:
        score -= 25
    if avg_cash < 50000:
        score -= 25

    score = max(score, 0)

    if score >= 75:
        risk = "Low Risk"
    elif score >= 50:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    # -------- Dashboard ----------
    st.subheader("📈 Key Metrics")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"{total_revenue:,}")
    c2.metric("Total Profit", f"{total_profit:,}")
    c3.metric("Profit Margin %", round(profit_margin, 2))
    c4.metric("Risk Level", risk)

    st.progress(score / 100)
    st.write(f"Financial Health Score: **{score}/100**")

    # -------- Chart ----------
    st.subheader("📉 Revenue vs Expenses Trend")

    fig, ax = plt.subplots()
    ax.plot(df["month"], df["revenue"])
    ax.plot(df["month"], df["expenses"])
    ax.legend(["Revenue", "Expenses"])
    st.pyplot(fig)

    # -------- Anomaly Detection ----------
    st.subheader("⚠️ Expense Anomaly Detection")

    exp_mean = df["expenses"].mean()
    exp_std = df["expenses"].std()

    anomalies = df[df["expenses"] > exp_mean + exp_std]

    if len(anomalies) > 0:
        st.warning("Unusual expense spikes detected:")
        st.dataframe(anomalies[["month", "expenses"]])
    else:
        st.success("No major expense anomalies detected.")
    
        # -------- Simple Forecast ----------
    st.subheader("🔮 Revenue Forecast (Next Month Projection)")

    if len(df) >= 2:
        growth_rates = df["revenue"].pct_change().dropna()
        avg_growth = growth_rates.mean()

        last_revenue = df["revenue"].iloc[-1]
        forecast_revenue = last_revenue * (1 + avg_growth)

        st.info(f"Estimated Next Month Revenue: {forecast_revenue:,.0f}")
        st.caption("Forecast based on average historical growth trend.")
    else:
        st.write("Not enough data for forecast.")


    # -------- AI Insight Engine ----------
    def ai_report(score, pm, er, dr, risk):

        en = []
        ta = []

        if pm < 15:
            en.append("Improve profit margins.")
            ta.append("லாப விகிதத்தை உயர்த்தவும்.")

        if er > 75:
            en.append("Reduce operating costs.")
            ta.append("செலவுகளை குறைக்கவும்.")

        if dr > 20:
            en.append("Debt levels are high.")
            ta.append("கடன் சுமை அதிகம்.")

        if score >= 75:
            en.append("Business is financially stable.")
            ta.append("வணிகம் நிதி ரீதியாக நிலையாக உள்ளது.")

        report_en = f"""
Risk Level: {risk}
Financial Score: {score}/100

Profit Margin: {pm:.2f}%
Expense Ratio: {er:.2f}%
Debt Ratio: {dr:.2f}%

AI Recommendations:
- """ + "\n- ".join(en)

        report_ta = f"""
அபாய நிலை: {risk}
நிதி மதிப்பெண்: {score}/100

லாப விகிதம்: {pm:.2f}%
செலவு விகிதம்: {er:.2f}%
கடன் விகிதம்: {dr:.2f}%

AI பரிந்துரைகள்:
- """ + "\n- ".join(ta)

        return report_en, report_ta

    rep_en, rep_ta = ai_report(score, profit_margin, expense_ratio, debt_ratio, risk)

    st.subheader("🤖 AI Financial Report — English")
    st.text(rep_en)

    st.subheader("🌍 AI Financial Report — Tamil")
    st.text(rep_ta)
