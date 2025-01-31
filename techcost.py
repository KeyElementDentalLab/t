import streamlit as st
import pandas as pd
import os

# Load or create data files
def load_data(file_name):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    return pd.DataFrame()

def save_data(df, file_name):
    df.to_csv(file_name, index=False)

# File paths for saving data
pnl_file = "pnl_data.csv"
technician_file = "technician_data.csv"
forecast_file = "forecast_data.csv"

# Load existing data
pnl_data = load_data(pnl_file)
technician_data = load_data(technician_file)
forecast_data = load_data(forecast_file)

# Streamlit UI
st.set_page_config(page_title="Dental Lab Profitability App", layout="wide")
st.title("Dental Lab Profitability Dashboard")

# Legal Notice Section
with st.expander("⚠ Notice: Intellectual Property & Legal Protection"):
    st.write("""
    This website and its underlying concepts, designs, features, and functionalities are the exclusive property of Santiago Escobar / Key Element Dental Laboratory LLC. Unauthorized access, reproduction, distribution, or replication of any part of this site, including but not limited to its design, code, and business model, is strictly prohibited.
    
    **Intellectual Property Rights:**
    All content, trademarks, and proprietary materials displayed or used on this site are protected under applicable copyright, trademark, and intellectual property laws.
    
    **Confidentiality & Restricted Use:**
    Any individual or entity accessing this site acknowledges that its contents, including but not limited to features, UI/UX, and business operations, are confidential and intended solely for private development and testing. Unauthorized disclosure, duplication, or replication of this project may result in legal action.
    
    **Legal Recourse & Enforcement:**
    Santiago Escobar / Key Element Dental Laboratory LLC retains full rights to pursue legal remedies, including but not limited to cease-and-desist orders, financial damages, and injunctions, against any party that copies, misuses, or attempts to claim ownership over this project, in full or in part.
    
    By continuing to access this site, you agree to these terms and acknowledge the proprietary rights of Santiago Escobar / Key Element Dental Laboratory LLC.
    """)

# Tabs Navigation
tabs = ["P&L Sheet", "Technician Profitability Calculator", "Profit Forecasting"]
selected_tab = st.radio("Select Module:", tabs)

if selected_tab == "P&L Sheet":
    st.header("Profitability Per Case Type")
    case_data = []
    case_types = ["Crowns", "Implants", "Bridges"]
    variable_case_type = st.text_input("Enter a Custom Case Type:")
    if variable_case_type:
        case_types.append(variable_case_type)
    
    for case_type in case_types:
        with st.expander(f"{case_type} Details"):
            st.subheader(f"{case_type} Revenue & Costs")
            price = st.number_input(f"Price per {case_type} ($)", min_value=0.0, step=10.0)
            quantity = st.number_input(f"Number of {case_type} Sold", min_value=0)
            revenue = price * quantity
            material_cost = st.number_input(f"Material Cost for {case_type} ($)", min_value=0.0, step=100.0)
            labor_cost = st.number_input(f"Labor Cost for {case_type} ($)", min_value=0.0, step=100.0)
            total_expenses = material_cost + labor_cost
            profit = revenue - total_expenses
            margin = (profit / revenue) * 100 if revenue else 0
            case_data.append({"Case Type": case_type, "Revenue ($)": revenue, "Material Cost ($)": material_cost,
                              "Labor Cost ($)": labor_cost, "Total Expenses ($)": total_expenses,
                              "Profit ($)": profit, "Profit Margin (%)": margin})
    
    # Display Summary Table in Columns
    st.header("Profitability Summary")
    col1, col2, col3 = st.columns(3)
    data = pd.DataFrame(case_data)
    col1.write("### Revenue & Costs")
    col1.dataframe(data[["Case Type", "Revenue ($)", "Total Expenses ($)"]])
    col2.write("### Profit Breakdown")
    col2.dataframe(data[["Case Type", "Profit ($)", "Profit Margin (%)"]])
    col3.write("### Detailed Costs")
    col3.dataframe(data[["Case Type", "Material Cost ($)", "Labor Cost ($)"]])
    
    if st.button("Save P&L Data"):
        pnl_data = pd.concat([pnl_data, data], ignore_index=True)
        save_data(pnl_data, pnl_file)
        st.success("P&L Data Saved Successfully!")

elif selected_tab == "Technician Profitability Calculator":
    st.header("Technician Profitability Calculator")
    salary = st.number_input("Technician Salary ($/month)", min_value=0.0, step=100.0)
    cases_per_month = st.number_input("Cases Produced Per Month", min_value=0)
    revenue_per_case = st.number_input("Revenue Per Case ($)", min_value=0.0, step=10.0)
    material_cost_per_case = st.number_input("Material Cost Per Case ($)", min_value=0.0, step=10.0)
    training_cost = st.number_input("Training & Benefits ($/month)", min_value=0.0, step=10.0)
    total_revenue = cases_per_month * revenue_per_case
    total_costs = salary + (cases_per_month * material_cost_per_case) + training_cost
    profit = total_revenue - total_costs
    st.metric("Technician Profitability ($)", f"${profit:,.2f}")
    
    if st.button("Save Technician Data"):
        technician_data = pd.concat([technician_data, pd.DataFrame([{"Salary": salary, "Cases Per Month": cases_per_month, "Revenue Per Case": revenue_per_case,
                                                 "Material Cost Per Case": material_cost_per_case, "Training Cost": training_cost, "Profitability": profit}])], ignore_index=True)
        save_data(technician_data, technician_file)
        st.success("Technician Data Saved Successfully!")

elif selected_tab == "Profit Forecasting":
    st.header("Profit Forecasting Tool")
    forecast_months = st.slider("Forecast Period (Months)", 1, 24, 12)
    future_salary = st.number_input("Future Technician Salary ($/month)", min_value=0.0, step=100.0)
    future_cases = st.number_input("Projected Cases Per Month", min_value=0)
    future_revenue_per_case = st.number_input("Projected Revenue Per Case ($)", min_value=0.0, step=10.0)
    future_material_cost = st.number_input("Projected Material Cost Per Case ($)", min_value=0.0, step=10.0)
    future_training = st.number_input("Projected Training & Benefits ($/month)", min_value=0.0, step=10.0)
    projected_profit = ((future_cases * future_revenue_per_case) - (future_salary + (future_cases * future_material_cost) + future_training)) * forecast_months
    st.metric("Projected Profit Over Time ($)", f"${projected_profit:,.2f}")
    
    if st.button("Save Forecast Data"):
        forecast_data = pd.concat([forecast_data, pd.DataFrame([{"Months": forecast_months, "Salary": future_salary, "Cases Per Month": future_cases,
                                              "Revenue Per Case": future_revenue_per_case, "Material Cost Per Case": future_material_cost,
                                              "Training Cost": future_training, "Projected Profit": projected_profit}])], ignore_index=True)
        save_data(forecast_data, forecast_file)
        st.success("Forecast Data Saved Successfully!")

