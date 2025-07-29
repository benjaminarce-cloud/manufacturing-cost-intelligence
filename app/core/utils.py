import pandas as pd
import streamlit as st
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_and_validate_data():
    """
    Loads all data from CSV files and performs critical validation checks.
    """
    try:
        bom_df = pd.read_csv("data/bom_products.csv")
        costs_df = pd.read_csv("data/manual_cost_drivers.csv")
        logging.info("Successfully loaded data files.")

        if costs_df.duplicated(subset=['CostDriver', 'Region']).any():
            raise ValueError("Duplicate (CostDriver, Region) pairs found in manual_cost_drivers.csv.")
        
        # --- THIS IS THE FIX ---
        # The validation now compares the BOM's 'Unit' with the cost file's 'Per_Unit'.
        merged_df = pd.merge(
            bom_df[['Component', 'Unit']],
            costs_df[['CostDriver', 'Per_Unit']],
            left_on='Component',
            right_on='CostDriver',
        )
        unit_mismatches = merged_df[merged_df['Unit'] != merged_df['Per_Unit']]
        if not unit_mismatches.empty:
            mismatch_str = unit_mismatches[['Component', 'Unit', 'Per_Unit']].to_string(index=False)
            raise ValueError(f"Unit mismatch found between BOM and cost drivers:\n{mismatch_str}")
        # --- END OF FIX ---
        
        logging.info("Data validation passed.")
        return bom_df, costs_df

    except FileNotFoundError as e:
        st.error(f"Error: A required data file was not found. Please check the 'data' folder. Details: {e}")
        logging.error(f"Data file not found: {e}")
        return pd.DataFrame(), pd.DataFrame()
    except ValueError as e:
        st.error(f"Data Validation Error: {e}")
        logging.error(f"Data validation failed: {e}")
        return pd.DataFrame(), pd.DataFrame()