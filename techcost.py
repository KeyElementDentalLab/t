import streamlit as st

def calculate_technician_labor():
    st.title("Technician Labor Cost Calculator")
    
    num_technicians = st.number_input("Number of Technicians", min_value=1, step=1, value=1)
    
    total_labor_cost = 0
    for i in range(num_technicians):
        st.subheader(f"Technician {i+1}")
        name = st.text_input(f"Technician {i+1} Name (Optional)")
        hourly_wage = st.number_input(f"Hourly Wage for Technician {i+1} ($/hour)", min_value=0.0, format="%.2f")
        hours_worked = st.number_input(f"Total Hours Worked per Day by Technician {i+1}", min_value=0.0, format="%.2f")
        units_produced = st.number_input(f"Number of Units Produced per Day by Technician {i+1}", min_value=1, step=1)
        overhead_percentage = st.number_input(f"Overhead & Taxes (%) for Technician {i+1}", min_value=0.0, format="%.2f")
        
        if units_produced > 0:
            daily_labor_cost = hourly_wage * hours_worked
            labor_cost_per_unit = daily_labor_cost / units_produced
            adjusted_cost_per_unit = labor_cost_per_unit * (1 + (overhead_percentage / 100))
            
            st.write(f"**Labor Cost per Unit for Technician {i+1}:** ${labor_cost_per_unit:.2f}")
            st.write(f"**Adjusted Cost per Unit (Including Overhead) for Technician {i+1}:** ${adjusted_cost_per_unit:.2f}")
            
            total_labor_cost += adjusted_cost_per_unit * units_produced
    
    st.subheader("Total Labor Cost Summary")
    st.write(f"**Total Daily Labor Cost Across All Technicians:** ${total_labor_cost:.2f}")

if __name__ == "__main__":
    calculate_technician_labor()