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
