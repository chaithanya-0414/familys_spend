import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
# Toggle between db (local sqlite) and db_sheets (google sheets)
import db_sheets as db 
# import db as db
st.set_page_config(page_title="FamilySpend", page_icon="💰", layout="wide")

# --- CUSTOM CSS ---
def inject_custom_css():
    with open('streamlit_style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- INIT ---
if 'db_initialized' not in st.session_state:
    db.init_db()
    db.seed_data()
    st.session_state['db_initialized'] = True

inject_custom_css()

# --- SIDEBAR & NAV ---
# Sidebar Styling
st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; margin-bottom: 0;">FamilySpend</h1>
        <p style="color: #718096; font-size: 0.8rem;">Smart Expense Tracker</p>
    </div>
""", unsafe_allow_html=True)

profiles = db.get_profiles()
profile_map = {p['display_name']: p['id'] for p in profiles}
selected_profile_name = st.sidebar.selectbox("👤 Current User", list(profile_map.keys()))
selected_profile_id = profile_map[selected_profile_name]

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "➕ Add Expense", "📝 History", "💳 Cards", "👪 Family View"])

# --- HELPERS ---
def card_metric(label, value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# --- PAGES ---

if page == "📊 Dashboard":
    st.markdown(f"## Welcome back, <span style='color:#667eea'>{selected_profile_name}</span>!", unsafe_allow_html=True)
    
    # Filter
    col_filter, _ = st.columns([2, 5])
    with col_filter:
        period = st.selectbox("Time Period", ["Month", "Week", "Year"])
    
    stats = db.get_dashboard_stats(selected_profile_id, period.lower())
    
    # Scorecards
    c1, c2, c3 = st.columns(3)
    with c1:
        card_metric("Total Spent", f"₹{stats['total_spent']:,.0f}")
    with c2:
        # Placeholder for Budget
        projections = stats['total_spent'] * 1.1 # Dummy projection
        card_metric("Projected", f"₹{projections:,.0f}")
    with c3:
        # Most spent category
        top_cat = "N/A"
        if stats['category_breakdown']:
            top_cat = stats['category_breakdown'][0]['name']
        card_metric("Top Category", top_cat)

    # Charts
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown("### 🍩 Spending Breakdown")
        if stats['category_breakdown']:
            df = pd.DataFrame(stats['category_breakdown'])
            fig = px.donut(df, values='total', names='name', hole=0.6,
                           color_discrete_sequence=px.colors.sequential.Bluyl)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font={'color': '#2d3748'}, showlegend=False)
            # Add center text
            fig.add_annotation(text=f"₹{stats['total_spent']/1000:.1f}k", 
                               x=0.5, y=0.5, showarrow=False, 
                               font=dict(size=20, color="#2d3748", family="Inter"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet.")

    with c2:
        st.markdown("### 📈 Weekly Trend")
        if stats['weekly_trend']:
            df = pd.DataFrame(stats['weekly_trend'])
            fig = px.bar(df, x='date', y='amount', color_discrete_sequence=['#667eea'])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font={'color': '#718096'},
                              xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#e2e8f0'))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet.")


elif page == "➕ Add Expense":
    st.markdown("## 💸 Add New Expense")
    
    with st.container():
        # Using a container to center heavily or just standard form
        with st.form("add_exp", clear_on_submit=True):
            cols = st.columns([1, 1])
            amount = cols[0].number_input("Amount (₹)", min_value=1.0, step=10.0, value=100.0)
            date = cols[1].date_input("Date", datetime.now())
            
            cats = db.get_categories()
            # Custom formatter for selectbox
            cat_opts = [f"{c['icon']} {c['name']}" for c in cats]
            cat_map = {f"{c['icon']} {c['name']}": c['id'] for c in cats}
            
            category = st.selectbox("Category", cat_opts)
            note = st.text_input("Note / Description", placeholder="e.g. Dinner at Paradise")
            
            cards = db.get_credit_cards(selected_profile_id)
            card_opts = ["💵 Cash / UPI"] + [f"💳 {c['card_name']}" for c in cards]
            card_map_opts = {f"💳 {c['card_name']}": c['id'] for c in cards}
            
            pay_mode = st.selectbox("Payment Mode", card_opts)
            
            submitted = st.form_submit_button("SAVE EXPENSE")
            
            if submitted:
                cat_id = cat_map[category]
                c_id = card_map_opts.get(pay_mode)
                if db.add_expense(selected_profile_id, cat_id, amount, date.strftime("%Y-%m-%d"), note, c_id):
                    st.toast("Expense Added Successfully!", icon="✅")
                else:
                    st.error("Error saving expense.")

elif page == "📝 History":
    st.markdown("## 📜 Transaction History")
    
    # Filter Row
    fc1, fc2, fc3 = st.columns([2, 2, 3])
    start = fc1.date_input("From", datetime.now().replace(day=1))
    end = fc2.date_input("To", datetime.now())
    
    exps = db.get_expenses(selected_profile_id, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
    
    if not exps:
        st.info("No transaction history found.")
    else:
        for e in exps:
            # Render custom HTML for card
            with st.container():
                
                # We use columns to integrate the Streamlit button native functionality with custom HTML
                # Custom HTML for the look
                html = f"""
                <div class="expense-item">
                    <div style="display:flex; align-items:center;">
                        <div class="expense-icon">{e['category_icon']}</div>
                        <div class="expense-details">
                            <div class="expense-cat">{e['category_name']} <span style="font-size:0.8em; color:#718096">({e['category_name_te']})</span></div>
                            <div class="expense-meta">{e['note'] if e['note'] else 'No note'} • {e['card_name'] if e['card_name'] else 'Cash'}</div>
                        </div>
                    </div>
                    <div style="text-align:right">
                         <div class="expense-amount">₹{e['amount']:,.0f}</div>
                         <div class="expense-date">{e['date']}</div>
                    </div>
                </div>
                """
                st.markdown(html, unsafe_allow_html=True)
                
                # Delete button (Small and unobtrusive)
                col_del, _ = st.columns([1, 8])
                if col_del.button("Delete", key=f"del_{e['id']}", help="Remove this entry"):
                    if db.delete_expense(e['id']):
                        st.toast("Expense deleted")
                        st.rerun()

elif page == "💳 Cards":
    st.markdown("## 💳 Credit Cards")
    
    # New Card Form Expander
    with st.expander("➕ Add New Credit Card"):
        with st.form("new_card"):
            gc1, gc2 = st.columns(2)
            name = gc1.text_input("Card Name", placeholder="HDFC Regalia")
            l4 = gc2.text_input("Last 4 Digits", max_chars=4, placeholder="1234")
            
            gc3, gc4 = st.columns(2)
            limit = gc3.number_input("Limit (₹)", step=5000)
            bill = gc4.number_input("Billing Day", 1, 31, 10)
            
            if st.form_submit_button("Add Card"):
                if db.add_credit_card(selected_profile_id, name, limit, bill, l4):
                    st.toast("Card Added!")
                    st.rerun()

    current_cards = db.get_credit_cards(selected_profile_id)
    if current_cards:
        for c in current_cards:
            # CSS class based on logic from original script.js if needed, or just standard gradients
            card_gradient = c['card_color'] if c['card_color'] else 'gradient-primary'
            if '#' in card_gradient: # if it is hex
                 bg_style = f"background: linear-gradient(135deg, {card_gradient} 0%, #000 100%);"
            else:
                 # Map legacy internal names to CSS classes or generic gradient
                 bg_style = "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"

            st.markdown(f"""
            <div class="credit-card-item" style="{bg_style}">
                <div class="card-header">
                    <div>
                        <div class="card-name">{c['card_name']}</div>
                        <div class="card-number">**** {c['card_last_four']}</div>
                    </div>
                    <div style="font-size: 1.5rem;">💳</div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:end;">
                    <div>
                        <div class="card-balance-label">Credit Limit</div>
                        <div class="card-balance-amount">₹{c['credit_limit']:,.0f}</div>
                    </div>
                    <div style="text-align:right">
                         <div style="font-size:0.8rem; opacity:0.9;">Billing Day</div>
                         <div>{c['billing_day']}th</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Delete {c['card_name']}", key=f"dc_{c['id']}"):
                db.delete_credit_card(c['id'])
                st.rerun()

elif page == "👪 Family View":
    st.markdown("## 🏡 Family Overview")
    
    period = st.selectbox("Period", ["Month", "Year"])
    data = db.get_family_overview(period.lower())
    
    card_metric("Total Family Spend", f"₹{data['total_family']:,.0f}")
    
    c1, c2 = st.columns(2)
    with c1:
         st.markdown("### 🏆 Top Spenders")
         if data['profile_spending']:
             df = pd.DataFrame(data['profile_spending'])
             fig = px.bar(df, x='display_name', y='total', color='total', text_auto='.2s',
                          color_continuous_scale='Bluyl')
             fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font={'color': '#2d3748'}, xaxis_title=None, yaxis_title=None,
                               coloraxis_showscale=False)
             st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.markdown("### 🍔 Where is it used?")
        if data['top_categories']:
            df = pd.DataFrame(data['top_categories'])
            fig = px.pie(df, values='total', names='name', hole=0.5,
                         color_discrete_sequence=px.colors.sequential.Bluyl)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font={'color': '#2d3748'}, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
