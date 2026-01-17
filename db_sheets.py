import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# --- CONSTANTS ---
# Using a single sheet with multiple worksheets
# Worksheets: profiles, categories, credit_cards, expenses
# We will use st.connection for caching and management

def get_conn():
    return st.connection("gsheets", type=GSheetsConnection)

def init_db():
    conn = get_conn()
    try:
        # We try to read a known worksheet to see if initialization is needed.
        # Note: In a real scenario, we might just assume the user sets up the sheet manually 
        # or we try to write empty DFs if they don't exist.
        # For simplicity and robustness with gsheets connection, we'll try to read.
        # If it fails, we might prompt user or just handle empty data in getters.
        pass
    except Exception:
        pass

def _read_df(worksheet, expected_cols):
    conn = get_conn()
    try:
        df = conn.read(worksheet=worksheet, ttl=0) # ttl=0 for fresh data
        # Ensure correct columns exist
        for col in expected_cols:
            if col not in df.columns:
                df[col] = None 
        return df
    except Exception:
        # Return empty DF with expected columns if sheet not found/empty
        return pd.DataFrame(columns=expected_cols)

def _write_df(worksheet, df):
    conn = get_conn()
    conn.update(worksheet=worksheet, data=df)

# --- PROFILES ---
def get_profiles():
    # Fallback/Default profiles if sheet is empty
    defaults = [
        {'id': 1, 'name': 'dad', 'display_name': 'Dad'},
        {'id': 2, 'name': 'mom', 'display_name': 'Mom'},
        {'id': 3, 'name': 'chaithu', 'display_name': 'Chaithu'},
        {'id': 4, 'name': 'harshith', 'display_name': 'Harshith'},
        {'id': 5, 'name': 'common', 'display_name': 'Common'}
    ]
    cols = ['id', 'name', 'display_name']
    df = _read_df('profiles', cols)
    
    if df.empty:
        df = pd.DataFrame(defaults)
        _write_df('profiles', df)
        return defaults
    
    return df.to_dict('records')

# --- CATEGORIES ---
def get_categories():
    # Defaults
    defaults = [
        {'id': 1, 'name': 'Rice', 'name_te': 'బియ్యం', 'icon': '🍚'},
        {'id': 2, 'name': 'Vegetables', 'name_te': 'కూరగాయలు', 'icon': '🥬'},
        {'id': 3, 'name': 'Fruits', 'name_te': 'పండ్లు', 'icon': '🍎'},
        {'id': 4, 'name': 'Dairy', 'name_te': 'పాల ఉత్పత్తులు', 'icon': '🥛'},
        {'id': 5, 'name': 'Fuel', 'name_te': 'ఇంధనం', 'icon': '⛽'},
        {'id': 6, 'name': 'Dining Out', 'name_te': 'బయట భోజనం', 'icon': '🍽️'},
        {'id': 7, 'name': 'Groceries', 'name_te': 'కిరాణా', 'icon': '🛒'},
        {'id': 8, 'name': 'Utilities', 'name_te': 'బిల్లులు', 'icon': '💡'},
        {'id': 9, 'name': 'Medical', 'name_te': 'వైద్యం', 'icon': '💊'},
        {'id': 10, 'name': 'Entertainment', 'name_te': 'వినోదం', 'icon': '🎬'},
        {'id': 11, 'name': 'Shopping', 'name_te': 'షాపింగ్', 'icon': '🛍️'},
        {'id': 12, 'name': 'Other', 'name_te': 'ఇతర', 'icon': '📦'}
    ]
    cols = ['id', 'name', 'name_te', 'icon']
    df = _read_df('categories', cols)
    
    if df.empty:
        df = pd.DataFrame(defaults)
        _write_df('categories', df)
        return defaults
        
    return df.to_dict('records')

# --- CREDIT CARDS ---
def get_credit_cards(profile_id=None):
    cols = ['id', 'profile_id', 'card_name', 'card_last_four', 'credit_limit', 'billing_day', 'card_color']
    df = _read_df('credit_cards', cols)
    
    if df.empty:
        return []
        
    if profile_id:
        df = df[df['profile_id'] == profile_id]
        
    return df.to_dict('records')

def add_credit_card(profile_id, card_name, credit_limit, billing_day, card_last_four='', card_color='#4A90E2'):
    cols = ['id', 'profile_id', 'card_name', 'card_last_four', 'credit_limit', 'billing_day', 'card_color', 'created_at']
    df = _read_df('credit_cards', cols)
    
    new_id = 1 if df.empty else df['id'].max() + 1
    new_card = {
        'id': new_id,
        'profile_id': profile_id,
        'card_name': card_name,
        'card_last_four': card_last_four,
        'credit_limit': credit_limit,
        'billing_day': billing_day,
        'card_color': card_color,
        'created_at': datetime.now().isoformat()
    }
    
    df = pd.concat([df, pd.DataFrame([new_card])], ignore_index=True)
    _write_df('credit_cards', df)
    return True

def delete_credit_card(card_id):
    cols = ['id', 'profile_id', 'card_name', 'card_last_four', 'credit_limit', 'billing_day', 'card_color', 'created_at']
    df = _read_df('credit_cards', cols)
    
    if df.empty:
        return False
        
    df = df[df['id'] != card_id]
    _write_df('credit_cards', df)
    
    # Also unlink expenses? In sheets, maybe just leave them or set to null. 
    # For now, we leave expenses as is to avoid complex multi-sheet updates if not critical.
    return True

# --- EXPENSES ---
def get_expenses(profile_id=None, start_date=None, end_date=None):
    cols = ['id', 'profile_id', 'category_id', 'amount', 'date', 'note', 'card_id', 'created_at']
    df = _read_df('expenses', cols)
    
    if df.empty:
        return []
        
    # Apply Filters
    if profile_id:
        df = df[df['profile_id'] == profile_id]
    
    if start_date:
        df = df[pd.to_datetime(df['date']) >= pd.to_datetime(start_date)]
        
    if end_date:
        df = df[pd.to_datetime(df['date']) <= pd.to_datetime(end_date)]
        
    # Join with Categories and Profiles for UI display
    # In SQLite we did JOINs. Here we do pandas merge or lookups.
    cats = {c['id']: c for c in get_categories()}
    profs = {p['id']: p for p in get_profiles()}
    cards = {c['id']: c for c in get_credit_cards()} # Helper to get all names
    
    res = []
    # Sort by date desc
    df = df.sort_values(by='date', ascending=False)
    
    for _, row in df.iterrows():
        c = cats.get(row['category_id'], {})
        p = profs.get(row['profile_id'], {})
        cc = cards.get(row['card_id'], {}) if pd.notna(row['card_id']) else {}
        
        res.append({
            'id': row['id'],
            'profile_id': row['profile_id'],
            'profile_name': p.get('display_name', 'Unknown'),
            'category_id': row['category_id'],
            'category_name': c.get('name', 'Unknown'),
            'category_name_te': c.get('name_te', ''),
            'category_icon': c.get('icon', '📝'),
            'amount': row['amount'],
            'date': row['date'],
            'note': row['note'],
            'card_id': row['card_id'],
            'card_name': cc.get('card_name', None)
        })
        
    return res

def add_expense(profile_id, category_id, amount, date, note='', card_id=None):
    cols = ['id', 'profile_id', 'category_id', 'amount', 'date', 'note', 'card_id', 'created_at']
    df = _read_df('expenses', cols)
    
    new_id = 1 if df.empty else df['id'].max() + 1
    new_exp = {
        'id': new_id,
        'profile_id': profile_id,
        'category_id': category_id,
        'amount': amount,
        'date': date,
        'note': note,
        'card_id': card_id if card_id else None,
        'created_at': datetime.now().isoformat()
    }
    
    df = pd.concat([df, pd.DataFrame([new_exp])], ignore_index=True)
    _write_df('expenses', df)
    return True

def delete_expense(expense_id):
    cols = ['id', 'profile_id', 'category_id', 'amount', 'date', 'note', 'card_id', 'created_at']
    df = _read_df('expenses', cols)
    
    if df.empty:
        return False
        
    df = df[df['id'] != expense_id]
    _write_df('expenses', df)
    return True

# --- DASHBOARD STATS ---
def get_dashboard_stats(profile_id, period='month'):
    # Re-use get_expenses to get filtered list then aggregate
    today = datetime.now()
    if period == 'week':
        start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    elif period == 'month':
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
    elif period == 'year':
        start_date = today.replace(month=1, day=1).strftime('%Y-%m-%d')
    else:
        start_date = None
        
    exps = get_expenses(profile_id, start_date=start_date)
    df = pd.DataFrame(exps)
    
    if df.empty:
        return {'total_spent': 0, 'category_breakdown': [], 'weekly_trend': []}
        
    total_spent = df['amount'].sum()
    
    # Cat breakdown
    cat_grp = df.groupby(['category_name', 'category_icon']).agg({'amount': 'sum'}).reset_index()
    cat_breakdown = []
    for _, row in cat_grp.sort_values('amount', ascending=False).iterrows():
        cat_breakdown.append({
            'name': row['category_name'],
            'icon': row['category_icon'],
            'total': row['amount']
        })
        
    # Weekly Trend (Daily for the period)
    trend_grp = df.groupby('date').agg({'amount': 'sum'}).reset_index().sort_values('date')
    weekly_trend = trend_grp.to_dict('records')
    
    return {
        'total_spent': total_spent,
        'category_breakdown': cat_breakdown,
        'weekly_trend': weekly_trend
    }

def get_family_overview(period='month'):
    today = datetime.now()
    if period == 'week':
        start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    elif period == 'month':
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
    else:
        start_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')
        
    exps = get_expenses(start_date=start_date)
    df = pd.DataFrame(exps)
    
    if df.empty:
        return {'total_family': 0, 'profile_spending': [], 'top_categories': []}
        
    total_family = df['amount'].sum()
    
    # By Profile
    prof_grp = df.groupby('profile_name').agg({'amount': 'sum'}).reset_index()
    profile_spending = []
    for _, row in prof_grp.sort_values('amount', ascending=False).iterrows():
        profile_spending.append({'display_name': row['profile_name'], 'total': row['amount']})
        
    # Top Categories
    cat_grp = df.groupby('category_name').agg({'amount': 'sum'}).reset_index()
    top_categories = []
    for _, row in cat_grp.sort_values('amount', ascending=False).head(10).iterrows():
        top_categories.append({'name': row['category_name'], 'total': row['amount']})
        
    return {
        'total_family': total_family,
        'profile_spending': profile_spending,
        'top_categories': top_categories
    }

# Seed data not really needed as we check defaults in getters
def seed_data():
    get_profiles()
    get_categories()
