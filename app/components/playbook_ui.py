import streamlit as st

def display_playbook(component_name, base_cost_per_unit, annual_volume):
    """
    Displays an interactive playbook of strategies for a given cost component.
    """
    # This dictionary is the "brain" of the Co-pilot's knowledge.
    playbooks = {
        "Machine Time": [
            {
                "name": "Increase Cycle Speed",
                "description": "Run the machine faster to produce more units in the same amount of time.",
                "slider_label": "Cycle Speed Improvement (%)",
            },
            {
                "name": "Reduce Setup/Changeover Time",
                "description": "Decrease the non-productive time between production runs.",
                "slider_label": "Setup Time Reduction (%)",
            }
        ],
        "Labor": [
            {
                "name": "Process Automation",
                "description": "Introduce robotics or automation to reduce the manual labor time per unit.",
                "slider_label": "Labor Time Reduction (%)",
            },
            {
                "name": "Operator Training Program",
                "description": "Invest in upskilling operators to improve efficiency and reduce errors.",
                "slider_label": "Efficiency Gain from Training (%)",
            }
        ],
         "Plastic": [
            {
                "name": "Negotiate with Suppliers",
                "description": "Leverage volume purchasing or longer-term contracts to secure a lower price per kg.",
                "slider_label": "Price Reduction (%)",
            },
            {
                "name": "Product Re-engineering (Light-weighting)",
                "description": "Redesign the product to use less material without compromising quality.",
                "slider_label": "Material Usage Reduction (%)",
            }
        ],
        # --- NEW KNOWLEDGE ADDED HERE ---
        "Cardboard": [
            {
                "name": "Negotiate with Suppliers",
                "description": "Leverage volume purchasing or longer-term contracts to secure a lower price per unit.",
                "slider_label": "Price Reduction (%)",
            },
            {
                "name": "Optimize Packaging Design (Right-Sizing)",
                "description": "Redesign the box to use less material while maintaining structural integrity.",
                "slider_label": "Material Usage Reduction (%)",
            }
        ],
        "Steel": [
            {
                "name": "Source Alternative Suppliers",
                "description": "Identify new or secondary suppliers to create price competition.",
                "slider_label": "Price Reduction (%)",
            },
            {
                "name": "Scrap Reduction Program",
                "description": "Implement quality controls to reduce the amount of wasted steel from the manufacturing process.",
                "slider_label": "Waste Reduction (%)",
            }
        ]
    }

    if component_name not in playbooks:
        st.warning(f"No specific playbook available for {component_name}.")
        return

    st.subheader(f"📈 Strategic Playbook for: {component_name}")

    for play in playbooks[component_name]:
        with st.container(border=True):
            st.markdown(f"**Play:** {play['name']}")
            st.caption(play['description'])
            
            improvement_pct = st.slider(play['slider_label'], 0, 100, 5, key=play['name'])
            
            col1, col2 = st.columns(2)
            project_cost = col1.number_input("Estimated Project Cost ($)", min_value=0, value=10000, step=1000, key=f"cost_{play['name']}")
            
            cost_saving_per_unit = base_cost_per_unit * (improvement_pct / 100.0)
            total_annual_savings = cost_saving_per_unit * annual_volume
            
            if project_cost > 0:
                roi_pct = (total_annual_savings - project_cost) / project_cost * 100
                payback_months = (project_cost / total_annual_savings) * 12 if total_annual_savings > 0 else 0
            else:
                roi_pct = float('inf')
                payback_months = 0
            
            col2.metric("Project ROI", f"{roi_pct:.1f}%")
            st.metric(
                label="Payback Period (Months)",
                value=f"{payback_months:.1f}" if payback_months > 0 else "Instant",
                help=f"Based on a projected annual savings of ${total_annual_savings:,.2f}"
            )