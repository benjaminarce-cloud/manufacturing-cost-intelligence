from app.core.cost_simulator import calculate_unit_cost

def test_calculate_unit_cost_with_breakdown(sample_data):
    """MEDIUM-PRIORITY: Unit test for the core cost calculation logic."""
    bom_df, _, cost_lookup = sample_data
    cost, breakdown = calculate_unit_cost("P1", bom_df, cost_lookup, "Texas")
    
    assert cost == 9.0 # (10 * 0.5) + (2 * 2.0)
    assert breakdown['Labor'] == 5.0
    assert breakdown['Steel'] == 4.0

def test_calculate_unit_cost_no_breakdown(sample_data):
    """Tests the performance optimization of not returning a breakdown."""
    bom_df, _, cost_lookup = sample_data
    cost = calculate_unit_cost("P1", bom_df, cost_lookup, "Texas", return_breakdown=False)
    assert cost == 9.0