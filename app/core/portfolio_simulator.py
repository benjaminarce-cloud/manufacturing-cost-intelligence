import pandas as pd
from .cost_simulator import calculate_unit_cost

def run_portfolio_simulation(bom_df, costs_df, change_scenario):
    """
    Calculates the total P&L impact of a single change across the entire product portfolio.
    """
    unique_products = bom_df.drop_duplicates(subset=['ProductID'])
    cost_lookup = {(row.CostDriver, row.Region): row.Rate for _, row in costs_df.iterrows()}

    total_baseline_profit = 0
    total_scenario_profit = 0
    product_impacts = []
    
    driver = change_scenario['driver']
    change_pct = change_scenario['change_pct']

    scenario_costs_df = costs_df.copy()
    scenario_costs_df.loc[scenario_costs_df['CostDriver'] == driver, 'Rate'] *= (1 + change_pct / 100)
    scenario_cost_lookup = {(row.CostDriver, row.Region): row.Rate for _, row in scenario_costs_df.iterrows()}

    for _, product in unique_products.iterrows():
        product_id = product['ProductID']
        annual_volume = product['AnnualVolume']
        selling_price = product['CurrentSellingPrice']
        region = product['Region']
        
        base_cost = calculate_unit_cost(product_id, bom_df, cost_lookup, region, return_breakdown=False)
        base_annual_profit = (selling_price - base_cost) * annual_volume

        scenario_cost = calculate_unit_cost(product_id, bom_df, scenario_cost_lookup, region, return_breakdown=False)
        scenario_annual_profit = (selling_price - scenario_cost) * annual_volume

        total_baseline_profit += base_annual_profit
        total_scenario_profit += scenario_annual_profit
        pnl_impact = scenario_annual_profit - base_annual_profit
        
        # --- THIS IS THE FIX ---
        # The 'Per Unit Impact' calculation has been restored.
        product_impacts.append({
            'ProductName': product['ProductName'],
            'P&L Impact': pnl_impact,
            'Per Unit Impact': (pnl_impact / annual_volume) if annual_volume > 0 else 0
        })
        # --- END OF FIX ---

    impact_df = pd.DataFrame(product_impacts)
    return total_baseline_profit, total_scenario_profit, impact_df.sort_values('P&L Impact', ascending=True)