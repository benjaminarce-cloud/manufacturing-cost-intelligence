import pandas as pd
from .cost_simulator import calculate_unit_cost

def analyze_portfolio_health(bom_df, costs_df):
    """
    Calculates the current profit margin for every product in the portfolio.
    """
    product_health = []
    unique_products = bom_df.drop_duplicates(subset=['ProductID'])

    # --- THIS IS THE FIX ---
    # We must pre-build the high-performance cost_lookup dictionary before the loop,
    # just like we do in the other simulator. This was the missing step.
    cost_lookup = {(row.CostDriver, row.Region): row.Rate for _, row in costs_df.iterrows()}
    # --- END OF FIX ---

    # Loop through each product.
    for _, product in unique_products.iterrows():
        product_id = product['ProductID']
        selling_price = product['CurrentSellingPrice']
        region = product['Region']
        
        # Now, we call the cost calculator with the correct 'cost_lookup' dictionary.
        cost, _ = calculate_unit_cost(product_id, bom_df, cost_lookup, region)
        
        # Calculate its margin in dollars and as a percentage.
        margin = selling_price - cost
        margin_pct = (margin / selling_price) * 100 if selling_price > 0 else 0
        
        product_health.append({
            'Product': product['ProductName'],
            'Margin (%)': margin_pct,
            'Margin ($)': margin
        })

    # Return a final table sorted by the most profitable products first.
    health_df = pd.DataFrame(product_health).sort_values('Margin (%)', ascending=False)
    return health_df