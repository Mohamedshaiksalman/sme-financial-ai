import pandas as pd

# -------------------------
# Load Financial Data
# -------------------------
df = pd.read_csv("sample_financials.csv")

print("Financial Data Loaded:")
print(df)

# -------------------------
# Compute Metrics
# -------------------------
total_revenue = df["revenue"].sum()
total_expenses = df["expenses"].sum()
total_profit = total_revenue - total_expenses
total_loans = df["loan_payment"].sum()
avg_cash = df["cash_in_bank"].mean()

profit_margin = (total_profit / total_revenue) * 100
expense_ratio = (total_expenses / total_revenue) * 100
debt_ratio = (total_loans / total_revenue) * 100

# -------------------------
# Financial Health Score
# -------------------------
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

# -------------------------
# Risk Level
# -------------------------
if score >= 75:
    risk = "Low Risk"
elif score >= 50:
    risk = "Moderate Risk"
else:
    risk = "High Risk"

print("\nKey Metrics:")
print("Total Revenue:", total_revenue)
print("Total Expenses:", total_expenses)
print("Total Profit:", total_profit)
print("Profit Margin %:", round(profit_margin, 2))
print("Expense Ratio %:", round(expense_ratio, 2))
print("Debt Ratio %:", round(debt_ratio, 2))
print("Financial Health Score:", score)
print("Risk Level:", risk)

# -------------------------
# Explainable AI Report Engine
# -------------------------
def generate_ai_report(score, pm, er, dr, risk):

    insights = []
    tamil = []

    if pm < 15:
        insights.append("Profit margin is low — improve pricing or product mix.")
        tamil.append("லாப விகிதம் குறைவு — விலை அல்லது பொருள் கலவை மேம்படுத்தவும்.")

    if er > 75:
        insights.append("Operating expenses are high — reduce unnecessary costs.")
        tamil.append("செலவுகள் அதிகம் — தேவையற்ற செலவுகளை குறைக்கவும்.")

    if dr > 20:
        insights.append("Debt burden is high — consider restructuring loans.")
        tamil.append("கடன் சுமை அதிகம் — கடனை மறுசீரமைக்கவும்.")

    if score >= 75:
        insights.append("Business shows strong financial stability.")
        tamil.append("வணிகம் நிதி ரீதியாக நிலையாக உள்ளது.")

    report_en = f"""
SME Financial Health AI Report

Risk Level: {risk}
Score: {score}/100

Profit Margin: {pm:.2f}%
Expense Ratio: {er:.2f}%
Debt Ratio: {dr:.2f}%

Recommendations:
- """ + "\n- ".join(insights)

    report_ta = f"""
SME நிதி ஆரோக்கிய AI அறிக்கை

அபாய நிலை: {risk}
மதிப்பெண்: {score}/100

லாப விகிதம்: {pm:.2f}%
செலவு விகிதம்: {er:.2f}%
கடன் விகிதம்: {dr:.2f}%

பரிந்துரைகள்:
- """ + "\n- ".join(tamil)

    return report_en, report_ta


rep_en, rep_ta = generate_ai_report(
    score, profit_margin, expense_ratio, debt_ratio, risk
)

print("\n--- AI Report (English) ---")
print(rep_en)

print("\n--- AI Report (Tamil) ---")
print(rep_ta)
