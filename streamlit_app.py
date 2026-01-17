import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import db

# Page Config
st.set_page_config(page_title="FamilySpend", page_icon="💰", layout="wide")

# Initialize DB
if 'db_initialized' not in st.session_state:
    db.init_db()
    db.seed_data()
    st.session_state['db_initialized'] = True

# Helper: Get Profiles (cached usually, but for simple app calling db is fine)
def load_profiles():
    return db.get_profiles()

def load_categories():
    return db.get_categories()

# Sidebar
st.sidebar.title("💰 FamilySpend")

profiles = load_profiles()
profile_names = [p['display_name'] for p in profiles]
profile_map = {p['display_name']: p['id'] for p in profiles}

# Profile Selector
selected_profile_name = st.sidebar.selectbox("👤 Select Profile", profile_names)
selected_profile_id = profile_map[selected_profile_name]
selected_profile_data = next(p for p in profiles if p['id'] == selected_profile_id)

st.sidebar.divider()

# Navigation
page = st.sidebar.radio("Navigation", ["Dashboard", "Add Expense", "History", "Credit Cards", "Family Overview"])

# --- DASHBOARD ---
if page == "Dashboard":
    st.title(f"Dashboard - {selected_profile_name}")
    
    # Period Filter
    period = st.selectbox("Period", ["Month", "Week", "Year"], index=0)
    period_key = period.lower()
    
    stats = db.get_dashboard_stats(selected_profile_id, period_key)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spent", f"₹{stats['total_spent']:,.0f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Category Breakdown")
        if stats['category_breakdown']:
            df_cat = pd.DataFrame(stats['category_breakdown'])
            fig_cat = px.pie(df_cat, values='total', names='name', title='Spending by Category', hole=0.4)
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("No data for this period.")
            
    with col2:
        st.subheader("Weekly Trend")
        if stats['weekly_trend']:
            df_trend = pd.DataFrame(stats['weekly_trend'])
            fig_trend = px.bar(df_trend, x='date', y='amount', title='Spending Trend (Last 7 Days)')
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No trend data.")

# --- ADD EXPENSE ---
elif page == "Add Expense":
    st.title("Add New Expense")
    
    with st.form("add_expense_form", clear_on_submit=True):
        categories = load_categories()
        cat_names = [f"{c['icon']} {c['name']} ({c['name_te']})" for c in categories]
        cat_map = {f"{c['icon']} {c['name']} ({c['name_te']})": c['id'] for c in categories}
        
        col1, col2 = st.columns(2)
        amount = col1.number_input("Amount (₹)", min_value=1.0, step=10.0)
        date = col2.date_input("Date", datetime.now())
        
        category_str = st.selectbox("Category", cat_names)
        note = st.text_input("Note (Optional)")
        
        # Credit Card Selection
        cards = db.get_credit_cards(selected_profile_id)
        card_options = ["None (Cash/Debit)"] + [f"{c['card_name']} (..{c['card_last_four']})" for c in cards]
        card_map = {f"{c['card_name']} (..{c['card_last_four']})": c['id'] for c in cards}
        card_choice = st.selectbox("Paid via Credit Card?", card_options)
        
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            cat_id = cat_map[category_str]
            card_id = card_map.get(card_choice) # Will be None if "None" selected
            
            success = db.add_expense(selected_profile_id, cat_id, amount, date.strftime('%Y-%m-%d'), note, card_id)
            if success:
                st.success("Expense added successfully!")
            else:
                st.error("Failed to add expense.")

# --- HISTORY ---
elif page == "History":
    st.title("Expense History")
    
    # Filters
    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start Date", datetime.now().replace(day=1))
    end_date = col2.date_input("End Date", datetime.now())
    
    expenses = db.get_expenses(selected_profile_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    
    if expenses:
        for ex in expenses:
            with st.container():
                c1, c2, c3, c4 = st.columns([1, 2, 2, 1])
                c1.write(f"**{ex['date']}**")
                c2.write(f"{ex['category_icon']} {ex['category_name']}")
                c3.write(f"₹{ex['amount']:,.0f}")
                if st.button("Delete", key=f"del_{ex['id']}"):
                    if db.delete_expense(ex['id']):
                        st.success("Deleted!")
                        st.rerun()
                if ex['note']:
                    st.caption(f"Note: {ex['note']}")
                st.divider()
    else:
        st.info("No expenses found for this period.")

# --- CREDIT CARDS ---
elif page == "Credit Cards":
    st.title("Credit Cards")
    
    with st.expander("Add New Card"):
        with st.form("add_card_form"):
            c_name = st.text_input("Card Name (e.g. HDFC Regalia)")
            c_last4 = st.text_input("Last 4 Digits", max_chars=4)
            c_limit = st.number_input("Credit Limit", min_value=0.0, step=1000.0)
            c_billing = st.number_input("Billing Day (1-31)", min_value=1, max_value=31)
            
            if st.form_submit_button("Add Card"):
                if db.add_credit_card(selected_profile_id, c_name, c_limit, c_billing, c_last4):
                    st.success("Card added!")
                    st.rerun()
    
    cards = db.get_credit_cards(selected_profile_id)
    if cards:
        for card in cards:
            st.subheader(f"{card['card_name']} (..{card['card_last_four']})")
            st.caption(f"Limit: ₹{card['credit_limit']:,.0f} | Billing Day: {card['billing_day']}")
            if st.button("Delete Card", key=f"del_card_{card['id']}"):
                if db.delete_credit_card(card['id']):
                    st.success("Card deleted!")
                    st.rerun()
            st.divider()
    else:
        st.info("No credit cards added yet.")

# --- FAMILY OVERVIEW ---
elif page == "Family Overview":
    st.title("Family Overview")
    
    period = st.selectbox("Period", ["Month", "Week", "Year"], key="fam_period")
    
    data = db.get_family_overview(period.lower())
    
    st.metric("Total Family Spending", f"₹{data['total_family']:,.0f}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Spending by Member")
        if data['profile_spending']:
            df_prof = pd.DataFrame(data['profile_spending'])
            fig_prof = px.bar(df_prof, x='display_name', y='total', title='Who spent what?')
            st.plotly_chart(fig_prof, use_container_width=True)
            
    with col2:
        st.subheader("Top Categories")
        if data['top_categories']:
            df_top = pd.DataFrame(data['top_categories'])
            fig_top = px.pie(df_top, values='total', names='name', title='Where is money going?')
            st.plotly_chart(fig_top, use_container_width=True)
