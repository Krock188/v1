import streamlit as st
from fpdf import FPDF
import base64
import matplotlib.pyplot as plt
import pandas as pd

# ─────────────── PAGE SETUP ───────────────
st.set_page_config(page_title="Private Retirement Blueprint", layout="wide")

# ─────────────── DARK MODE TOGGLE ───────────────
mode = st.toggle("🌙 Dark Mode", value=False)

# Inject card-style layout and dark mode CSS
st.markdown(
    f"""
    <style>
    .card {{
        background-color: #f9f9f9;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }}
    .dark-card {{
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(255, 255, 255, 0.05);
        margin-bottom: 2rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────── HEADER ───────────────
st.markdown("# Private Retirement Blueprint")
st.markdown("_A modern approach to building tax-free income with structured insurance_")
st.markdown("---")

# ─────────────── INPUT + OUTPUT LAYOUT ───────────────
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Scenario Inputs")
    st.markdown(f'<div class="{ "dark-card" if mode else "card" }">', unsafe_allow_html=True)

    annual_income = st.number_input("Annual Income", value=250000, step=10000)
    reposition_amount = st.number_input("Repositioned Amount (Annual)", value=50000, step=5000)
    product = st.selectbox("Product Type", ["Indexed UL", "Variable UL", "Whole Life", "Guaranteed UL"])
    growth_rate = st.slider("Growth Rate (%)", 3.0, 9.0, 6.0)
    years_funded = st.slider("Years of Contributions", 5, 30, 15)
    retirement_years = st.slider("Years of Retirement Income", 10, 40, 25)

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### Projected Results")
    st.markdown(f'<div class="{ "dark-card" if mode else "card" }">', unsafe_allow_html=True)

    total_contributions = reposition_amount * years_funded
    future_value = total_contributions * ((1 + growth_rate / 100) ** (retirement_years - years_funded))
    estimated_annual_income = future_value / retirement_years

    st.metric("Total Contributions", f"${total_contributions:,.0f}")
    st.metric("Projected Capital", f"${future_value:,.0f}")
    st.metric("Tax-Free Income", f"${estimated_annual_income:,.0f}")

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────── ROI DASHBOARD ───────────────
st.markdown("### 📊 Annual ROI Overview")
st.markdown(f'<div class="{ "dark-card" if mode else "card" }">', unsafe_allow_html=True)

years = list(range(1, years_funded + retirement_years + 1))
annual_contributions = [reposition_amount if y <= years_funded else 0 for y in years]
capital = []
value = 0
annual_rate = (1 + growth_rate / 100)

for c in annual_contributions:
    value = (value + c) * annual_rate
    capital.append(value)

cumulative_contrib = [sum(annual_contributions[:i+1]) for i in range(len(years))]
roi_percent = [
    round((cap - contrib) / contrib * 100, 2) if contrib > 0 else 0
    for cap, contrib in zip(capital, cumulative_contrib)
]

df_annual = pd.DataFrame({
    "Year": years,
    "Capital Value ($)": capital,
    "Cumulative Contributions ($)": cumulative_contrib,
    "ROI (%)": roi_percent
})

# Save chart as image
fig, ax = plt.subplots()
ax.plot(df_annual["Year"], df_annual["Capital Value ($)"], label="Capital Value", linewidth=2)
ax.plot(df_annual["Year"], df_annual["Cumulative Contributions ($)"], label="Contributions", linewidth=2, linestyle="--")
ax.set_xlabel("Year")
ax.set_ylabel("Value ($)")
ax.set_title("Capital vs. Contributions")
ax.legend()
plt.tight_layout()
chart_path = "roi_chart.png"
fig.savefig(chart_path)
plt.close()

st.line_chart(df_annual.set_index("Year")[["Capital Value ($)", "Cumulative Contributions ($)"]])
st.caption("Annualized performance view: Tracks capital growth vs. contributions with clear ROI pacing.")
st.markdown("</div>", unsafe_allow_html=True)

# ─────────────── PDF GENERATION ───────────────
st.markdown("### 📄 Download Report")
st.markdown(f'<div class="{ "dark-card" if mode else "card" }">', unsafe_allow_html=True)
st.write("Get a clean summary of your projection for offline review.")

def generate_pdf(total_contributions, future_value, estimated_annual_income):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Private Retirement Blueprint", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total Contributions: ${total_contributions:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Projected Capital: ${future_value:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Estimated Tax-Free Income: ${estimated_annual_income:,.2f}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="Projections assume tax-deferred growth and policy loan distributions under IRC §7702. Based on selected growth assumptions and retirement duration.")
    pdf.image(chart_path, x=10, y=pdf.get_y() + 10, w=180)
    return pdf.output(dest='S').encode('latin1')

pdf_data = generate_pdf(total_contributions, future_value, estimated_annual_income)
b64 = base64.b64encode(pdf_data).decode()
href = f'<a href="data:application/octet-stream;base64,{b64}" download="Private_Retirement_Blueprint.pdf">Download PDF Report</a>'
st.markdown(href, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

