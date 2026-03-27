import streamlit as st
import pandas as pd
import plotly.express as px

from utils import detect_leakages
from predictor import predict_future_risk

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Expense Leakage AI",
    page_icon="💸",
    layout="wide"
)

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
h1 {color:#ff4b4b;}
.card {
    background:#f8f9fa;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.title("💸 Expense Leakage & Financial Risk Intelligence")
st.caption("AI-powered system to detect invisible money leaks & future risk")

# ---------------- FILE UPLOAD ----------------
uploaded = st.sidebar.file_uploader("📥 Upload Transactions CSV", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("sample_transactions.csv")

# ---------------- COLUMN NORMALIZATION (CRITICAL FIX) ----------------
df.columns = df.columns.str.strip().str.lower()

# Detect date column automatically
date_col = None
for col in df.columns:
    if "date" in col:
        date_col = col
        break

if date_col is None:
    st.error("❌ No date column found in the uploaded file.")
    st.stop()

df.rename(columns={date_col: "date"}, inplace=True)

# Rename required columns safely
rename_map = {}
for col in df.columns:
    if "amount" in col:
        rename_map[col] = "amount"
    if "category" in col:
        rename_map[col] = "category"
    if "description" in col or "merchant" in col:
        rename_map[col] = "description"

df.rename(columns=rename_map, inplace=True)

required = {"date", "amount", "category", "description"}
if not required.issubset(df.columns):
    st.error("❌ CSV must contain Date, Amount, Category, Description columns")
    st.stop()

df["date"] = pd.to_datetime(df["date"])

# ---------------- METRICS ----------------
total_spent = df["amount"].sum()
avg_daily = df.groupby("date")["amount"].sum().mean()

c1, c2, c3 = st.columns(3)
c1.metric("💰 Total Spend", f"₹{int(total_spent)}")
c2.metric("📅 Avg Daily Spend", f"₹{int(avg_daily)}")
c3.metric("🧾 Transactions", len(df))

# ---------------- VISUALIZATION ----------------
st.subheader("📊 Category-wise Spending")
fig = px.pie(df, names="category", values="amount", hole=0.45)
st.plotly_chart(fig, use_container_width=True)

# ---------------- LEAKAGE DETECTION ----------------
st.subheader("🚨 Invisible Expense Leakages")
leaks = detect_leakages(df)

leak_total = 0
if leaks:
    for name, amt in leaks:
        st.warning(f"{name} → ₹{int(amt)}")
        leak_total += amt
else:
    st.success("✅ No major leakages detected")

# ---------------- DAMAGE REPORT ----------------
st.subheader("📉 Damage Report")
st.markdown(f"""
<div class="card">
<b>Total Hidden Leakage:</b> ₹{int(leak_total)}<br><br>
This money could be saved, invested, or used for emergencies.<br>
Small daily spends create large financial damage over time.
</div>
""", unsafe_allow_html=True)

# ---------------- FUTURE RISK PREDICTION ----------------
st.subheader("🔮 Future Financial Risk Prediction")
risk = predict_future_risk(df)

st.error(f"""
⚠ Predicted Average Daily Spend (Next 7 Days): ₹{risk}

If this trend continues, financial stress may increase.
""")

# ---------------- RECOMMENDATIONS ----------------
st.subheader("💡 Smart Recommendations")
st.success("""
✔ Reduce frequent small purchases  
✔ Cancel unused subscriptions  
✔ Set daily spending alerts  
✔ Review expenses weekly  
""")

st.caption("Prototype built for Hackathon • Behavioral Finance AI")
