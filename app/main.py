import streamlit as st
import pandas as pd
from core.utils import load_and_validate_data as load_data
from core.portfolio_simulator import run_portfolio_simulation
from core.portfolio_analyzer import analyze_portfolio_health
from core.llm_utils import generate_ai_report

# --- App Configuration & Data Loading ---
st.set_page_config(layout="wide", page_title="Corporate Co-pilot")

@st.cache_data
def load_all_data():
    """Loads all data from CSV files and caches it for performance."""
    bom_df, costs_df = load_data()
    return bom_df, costs_df

try:
    bom_df, costs_df = load_all_data()
    if bom_df.empty or costs_df.empty:
        st.error("Data loading failed. Please check the data files and refresh.")
        st.stop()
except Exception as e:
    st.error(f"A critical error occurred during data loading: {e}")
    st.stop()

# --- App Navigation ---
st.sidebar.title("🚀 Corporate Co-pilot")
page = st.sidebar.radio("Select Analysis Mode", 
    ["🏢 Corporate Scenario Planner", "📈 Product Portfolio Health"])

# ==============================================================================
# PAGE 1: CORPORATE SCENARIO PLANNER
# ==============================================================================
if page == "🏢 Corporate Scenario Planner":
    st.title("Corporate Scenario Planner")
    st.sidebar.header("Define a Company-Wide Change")

    drivers = costs_df['CostDriver'].unique()
    drivers_list = sorted(drivers.tolist())
    try:
        default_index = drivers_list.index("Semiconductors")
    except ValueError:
        default_index = 0
    selected_driver = st.sidebar.selectbox("Select Cost Driver to Change", drivers_list, index=default_index)
    
    change_percentage = st.sidebar.slider("Change Percentage (%)", -50, 50, 15)
    scenario_description = st.sidebar.text_input("Describe this scenario", f"{change_percentage}% increase in all {selected_driver} costs")

    base_profit, scenario_profit, impact_df = run_portfolio_simulation(bom_df, costs_df, {'driver': selected_driver, 'change_pct': change_percentage})
    total_pnl_impact = scenario_profit - base_profit

    st.header("Financial Impact Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("Baseline Annual Gross Profit", f"${base_profit:,.2f}")
    col2.metric("Scenario Annual Gross Profit", f"${scenario_profit:,.2f}")
    col3.metric("Total P&L Impact", f"${total_pnl_impact:,.2f}")

    st.subheader("Top 3 Most Affected Products")
    display_df = impact_df.head(3).copy()
    display_df['P&L Impact'] = display_df['P&L Impact'].apply(lambda x: f"${x:,.2f}")
    display_df['Per Unit Impact'] = display_df['Per Unit Impact'].apply(lambda x: f"${x:,.2f}")
    display_df.rename(columns={'ProductName': 'Product', 'P&L Impact': 'Total Profit Change ($)', 'Per Unit Impact': 'Per Unit Profit Change ($)'}, inplace=True)
    st.dataframe(display_df, hide_index=True, use_container_width=True)

    st.header("🤖 AI Strategic Briefing")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")

    if st.button("Generate AI Briefing"):
        if api_key:
            ai_df = display_df.copy()
            with st.spinner("The AI Strategist is preparing your briefing..."):
                report_text = generate_ai_report(
                    api_key,
                    scenario_desc=scenario_description,
                    base_profit=base_profit,
                    scenario_profit=scenario_profit,
                    top_3_products_df=ai_df,
                    costs_df=costs_df
                )
            if report_text:
                st.markdown("---")
                st.markdown(report_text, unsafe_allow_html=True)
        else:
            st.warning("Please enter your OpenAI API key.")

# ==============================================================================
# PAGE 2: PRODUCT PORTFOLIO HEALTH
# ==============================================================================
elif page == "📈 Product Portfolio Health":
    st.title("Product Portfolio Health")
    st.info("This page analyzes the current profitability of every product.")
    
    health_df = analyze_portfolio_health(bom_df, costs_df)
    
    # --- THIS IS THE FIX ---
    # Create the Top 3 "Stars" DataFrame from the original sorted data
    top_3_df = health_df.head(3).copy()
    top_3_df['Margin (%)'] = top_3_df['Margin (%)'].apply(lambda x: f"{x:.1f}%")
    top_3_df['Margin ($)'] = top_3_df['Margin ($)'].apply(lambda x: f"${x:,.2f}")

    # Create the Bottom 3 "At-Risk" DataFrame using the CORRECT sorting logic
    # Sort the ENTIRE dataframe ascending (worst to best) and THEN take the top 3
    bottom_3_df = health_df.sort_values('Margin (%)', ascending=True).head(3).copy()
    bottom_3_df['Margin (%)'] = bottom_3_df['Margin (%)'].apply(lambda x: f"{x:.1f}%")
    bottom_3_df['Margin ($)'] = bottom_3_df['Margin ($)'].apply(lambda x: f"${x:,.2f}")
    # --- END OF FIX ---

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⭐ Top 3 Most Profitable Products (Stars)")
        st.dataframe(top_3_df, hide_index=True, use_container_width=True)
    with col2:
        st.subheader("⚠️ Bottom 3 Least Profitable Products (At-Risk)")
        st.dataframe(bottom_3_df, hide_index=True, use_container_width=True)