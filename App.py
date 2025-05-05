import streamlit as st
from fpdf import FPDF
import base64

# ─────────────── PAGE SETUP ───────────────
st.set_page_config(page_title="Private Retirement Blueprint", layout="wide")

# ─────────────── DARK MODE TOGGLE ───────────────
mode = st.toggle("🌙 Dark Mode", value=False)

if mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #111111;
            color: #FAFAFA;
        }

        .css-18e3th9 {
            background-color: #111111 !important;
        }

        .css-1d391kg, .css-1avcm0n {
            background-color: #0e0e0e !important;
        }

        .stMarkdown h1, h2, h3, h4, h5, h6 {
            color: #ffffff;
        }

        .css-1cpxqw2, .css-ffhzg2 {
            color: #ffffff !important;
        }

        .stButton>button {
            background-color: #333;
            color: #FAFAFA;
            border: 1px solid #888;
            border-radius: 8px;
        }

        .stSelectbox>div>div {
            background-color: #222 !important;
            color: #FAFAFA !important;
        }

        .stSlider > div {
            color: #FAFAFA;
        }

        a {
            color: #4fa3f7 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ─────────────── HEADER ───────────────
st.markdown("# Private Retirement Blueprint")
st.markdown("_A modern approach to building tax-free income with structured insurance_")
st.markdown("---")

# ─────────────── SIDEBAR INPUTS ───────────────
st.sidebar.markdown("### Customize Your Scenario")

annual_income = st.sidebar.number_input("Annual Income", value=250000, step=10000)
reposition_amount = st.sidebar.number_input("Repositioned Amount (Annual)", value=50000, step=5000)
product = st.sidebar.selectbox("Product Type", ["Indexed UL", "Variable UL", "Whole Life", "Guaranteed UL"])
growth_rate = st.sidebar.slider("Growth Rate (%)", 3.0, 9.0, 6.0)
years_funded = st.sidebar.slider("Years of Contributions", 5, 30, 15)
retirement_years = st.sidebar.slider("Years of Retirement Income", 10, 40, 25)

# ─────────────── CALCULATIONS ───────────────
total_contributions = reposition_amount * years_funded
future_value = total_contributions * ((1 + growth_rate / 100) ** (retirement_years - years_funded))
estimated_annual_income = future_value / retirement_years

# ─────────────── OUTPUT METRICS ───────────────
st.markdown("## Results")
col1, col2, col3 = st.columns(3)
col1.metric("Total Contributions", f"${total_contributions:,.0f}")
col2.metric("Projected Capital", f"${future_value:,.0f}")
col3.metric("Tax-Free Income", f"${estimated_annual_income:,.0f}")

st.markdown("---")

# ─────────────── STRATEGY EXPLAINER ───────────────
with st.expander("About This Strategy"):
    st.markdown("""
    This tool models capital accumulation using structured insurance products like IUL, VUL, Whole Life, and GUL.
    
    It assumes tax-deferred growth and tax-free income via policy loans under **IRC §7702**. Results are illustrative and depend on actual policy design and carrier performance.
    """)

# ─────────────── PDF GENERATION FUNCTION ───────────────
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

    return pdf.output(dest='S').encode('latin1')

# ─────────────── PDF DOWNLOAD LINK ───────────────
st.markdown("### Download Report")
st.write("Get a clean summary of your projection for offline review.")

pdf_data = generate_pdf(total_contributions, future_value, estimated_annual_income)
b64 = base64.b64encode(pdf_data).decode()
href = f'<a href="data:application/octet-stream;base64,{b64}" download="Private_Retirement_Blueprint.pdf">Download PDF Report</a>'
st.markdown(href, unsafe_allow_html=True)

# ─────────────── ROI DASHBOARD ───────────────
import pandas as pd

st.markdown("## 📈 ROI Dashboard")

# Create monthly projection
months = list(range(1, years_funded + retirement_years + 1))
contributions = [reposition_amount if m <= years_funded else 0 for m in months]
capital = []
value = 0
monthly_rate = (growth_rate / 100) / 12

for c in contributions:
    value = (value + c) * (1 + monthly_rate)
    capital.append(value)

cumulative_contrib = [sum(contributions[:i+1]) for i in range(len(contributions))]
roi_percent = [
    round((cap - contrib) / contrib * 100, 2) if contrib > 0 else 0
    for cap, contrib in zip(capital, cumulative_contrib)
]

df = pd.DataFrame({
    "Month": months,
    "Capital Value ($)": capital,
    "Cumulative Contributions ($)": cumulative_contrib,
    "ROI (%)": roi_percent
})

st.line_chart(df.set_index("Month")[["Capital Value ($)", "Cumulative Contributions ($)"]])

st.caption("This chart shows your projected capital accumulation over time versus cumulative contributions, highlighting the ROI trajectory of your structured insurance strategy.")
