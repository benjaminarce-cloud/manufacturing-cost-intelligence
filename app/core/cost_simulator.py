def calculate_unit_cost(product_id, bom_df, cost_lookup, region, return_breakdown=True):
    """
    Calculates the per-unit cost of a single product using a high-performance dictionary lookup.
    """
    product_bom = bom_df[bom_df['ProductID'] == product_id]
    
    if product_bom.empty:
        return 0, {} if return_breakdown else 0

    cost_breakdown = {} if return_breakdown else None
    total_cost = 0.0

    for _, item in product_bom.iterrows():
        component = item['Component']
        quantity = item['Quantity']
        
        # MEDIUM-PRIORITY: Replaced DataFrame lookup with O(1) dictionary access
        # CRITICAL FIX: Removed hard-coded "Texas" by using a fallback lookup order
        rate = cost_lookup.get((component, region), cost_lookup.get((component, 'Default'), 0))

        cost = quantity * rate
        total_cost += cost
        
        # MEDIUM-PRIORITY: Avoid building the dictionary if not needed
        if return_breakdown:
            cost_breakdown[component] = cost
    
    return (total_cost, cost_breakdown) if return_breakdown else total_cost