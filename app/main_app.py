import sys
import os
import streamlit as st

# 1. Setup Path (Crucial for importing from src)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.optimizer import calculate_inventory_metrics, get_item_catalog

# 2. Page Configuration
st.set_page_config(page_title="Retail Inventory Pro", page_icon="📦", layout="wide")

# 3. Initialize Catalog in Session State
if 'catalog' not in st.session_state:
    st.session_state.catalog = get_item_catalog()

# 4. SIDEBAR: Management Tools
st.sidebar.title("🛠️ Admin Controls")

# Feature: Add Item
with st.sidebar.expander("➕ Add New Product"):
    new_item = st.text_input("Product Name")
    if st.button("Add to Catalog"):
        if new_item and new_item not in st.session_state.catalog:
            st.session_state.catalog.append(new_item)
            st.success(f"Added {new_item}")
            st.rerun()

# Feature: Rename Item
with st.sidebar.expander("📝 Rename Product"):
    target = st.selectbox("Select Target", st.session_state.catalog)
    rename_to = st.text_input("New Name")
    if st.button("Apply Rename"):
        if rename_to:
            idx = st.session_state.catalog.index(target)
            st.session_state.catalog[idx] = rename_to
            st.rerun()

# 5. MAIN UI: Dashboard
st.title("📦 Retail Sales Forecasting & Inventory Optimizer")
st.markdown("---")

# Layout: Selection and Inputs
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    selected_prod = st.selectbox("🎯 Target Product for Analysis", st.session_state.catalog)

with col2:
    forecast_val = st.number_input("Predicted Daily Demand", min_value=1, value=150)

with col3:
    lt_days = st.slider("Lead Time (Days)", 1, 14, 3)

# 6. Calculations
ss, rop = calculate_inventory_metrics(forecast_val, lt_days)

# 7. Display Results
st.write(f"### Analysis Results for: {selected_prod}")

metric_col1, metric_col2, metric_col3 = st.columns(3)

metric_col1.metric("Safety Stock (Buffer)", f"{ss} Units")
metric_col2.metric("Reorder Point (ROP)", f"{rop} Units")
metric_col3.metric("Lead Time Demand", f"{forecast_val * lt_days} Units")

st.info(f"📋 **Action Plan:** When the physical stock of **{selected_prod}** hits **{rop}** units, trigger a replenishment order.")

# 8. Visual Proof (Graph)
st.subheader("Inventory Strategy Visualization")
chart_data = {
    "Level": ["Safety Stock", "Demand During Lead Time", "Reorder Point"],
    "Units": [ss, (forecast_val * lt_days), rop]
}
st.bar_chart(chart_data, x="Level", y="Units")