import streamlit as st

# Page Setup
st.set_page_config(page_title="Private Retirement Blueprint", layout="wide")
st.title("Private Retirement Blueprint")
st.subheader("Calculate Your Potential Tax-Free Cash Flow")

# Sidebar Inputs
st.sidebar.header("Input Assumptions")
annual_income = st.sidebar.number_input("Annual Income ($)", value=250000, step=10000)
reposition_amount = st.sidebar.number_input("Amount Repositioned Annually ($)", value=50000, step=5000)
product = st.sidebar.selectbox("Product Type", ["Indexed UL", "Variable UL", "Whole Life", "Guaranteed UL"])
growth_rate = st.sidebar.slider("Expected Annual Growth Rate (%)", 3.0, 9.0, 6.0)
years_funded = st.sidebar.slider("Years of Contributions", 5, 30, 15)
retirement_years = st.sidebar.slider("Years of Retirement Income", 10, 40, 25)

# Backend Calculations
total_contributions = reposition_amount * years_funded
future_value = total_contributions * ((1 + growth_rate / 100) ** (retirement_years - years_funded))
estimated_annual_income = future_value / retirement_years

# Output Display
st.markdown("### Results")
st.metric("Total Contributions", f"${total_contributions:,.0f}")
st.metric("Projected Tax-Free Capital", f"${future_value:,.0f}")
st.metric("Estimated Annual Tax-Free Income", f"${estimated_annual_income:,.0f}")

with st.expander("How These Strategies Work"):
    st.markdown("""
    **How this works:**
    - Your annual contributions are assumed to grow at the selected rate.
    - The capital compounds tax-deferred.
    - At retirement, distributions are modeled as tax-free policy loans (under IRC §7702).

    **Product Highlights:**
    - *IUL*: Growth tied to an index, downside floor
    - *VUL*: Investment-driven with subaccount options
    - *Whole Life*: Guarantees + dividends
    - *GUL*: Low cash value, high death benefit
    """)

st.markdown("---")
st.markdown("**Want a personalized case design? Book a session.**")

from fpdf import FPDF
import base64

# Function to generate PDF
def generate_pdf(total_contributions, future_value, estimated_annual_income):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Private Retirement Blueprint", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total Contributions: ${total_contributions:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Projected Tax-Free Capital: ${future_value:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Estimated Annual Tax-Free Income: ${estimated_annual_income:,.2f}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="This projection assumes tax-deferred accumulation and tax-free distributions under IRC §7702 using structured life insurance strategies.")

    return pdf.output(dest='S').encode('latin1')

# Show Report Download Section
st.markdown("### Your PDF Report")
st.write("Download your personalized projection to review or share with your tax advisor.")

# Generate and display PDF download link
pdf_data = generate_pdf(total_contributions, future_value, estimated_annual_income)
b64 = base64.b64encode(pdf_data).decode()
href = f'<a href="data:application/octet-stream;base64,{b64}" download="Private_Retirement_Blueprint.pdf">📄 Download PDF Report</a>'
st.markdown(href, unsafe_allow_html=True)
