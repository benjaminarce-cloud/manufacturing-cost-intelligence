import streamlit as st
from openai import OpenAI
import pandas as pd
import random # For handling ties

def generate_ai_report(api_key, scenario_desc, base_profit, scenario_profit, top_3_products_df, costs_df):
    """
    Generates a high-level executive report using the OpenAI Chat API.
    """
    client = OpenAI(api_key=api_key)

    # HIGH-PRIORITY: Handle ties in feasibility by choosing randomly from the best
    max_feasibility = costs_df['Feasibility'].max()
    top_levers = costs_df[costs_df['Feasibility'] == max_feasibility]['CostDriver'].tolist()
    highest_feasibility_lever = random.choice(top_levers)

    top_products_str = top_3_products_df.to_string(index=False)

    # HIGH-PRIORITY: Switched to the Chat API with a system prompt for lower cost and better performance
    system_prompt = """
    You are a top-tier management consultant from a firm like McKinsey or BCG, briefing the CEO.
    Your analysis must be sharp, insightful, and go beyond the obvious first-order effects.
    Use markdown for all formatting. Your goal is to provide a high-leverage, non-obvious solution.
    """
    user_prompt = f"""
    **Analysis Request:**
    Provide a strategic briefing on the following scenario: "{scenario_desc}".

    **Key Data Points:**
    - Baseline Annual Gross Profit: ${base_profit:,.2f}
    - Scenario Annual Gross Profit: ${scenario_profit:,.2f}
    - Top 3 Most Financially Affected Products:
    {top_products_str}
    - Internal Feasibility Data Hint: Our data suggests that **'{highest_feasibility_lever}'** is the cost area with the highest operational feasibility for change.

    **Structure your briefing in three parts:**
    ### 1. The Bottom Line
    Concisely state the total financial damage.
    ### 2. The Core Problem
    Analyze if the damage is concentrated in the Top 3 products.
    ### 3. Strategic Recommendation: The Non-Obvious Path
    Provide your top recommendation. Justify your choice by connecting the immediate problem to a more systemic, feasible solution.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=700,
            temperature=0.6
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred with the OpenAI API: {e}")
        return None