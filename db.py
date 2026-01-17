import sqlite3
from datetime import datetime, timedelta

DATABASE = 'data.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Profiles table
    c.execute('''CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        display_name TEXT NOT NULL
    )''')
    
    # Categories table
    c.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        name_te TEXT NOT NULL,
        icon TEXT
    )''')
    
    # Credit Cards table
    c.execute('''CREATE TABLE IF NOT EXISTS credit_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_id INTEGER NOT NULL,
        card_name TEXT NOT NULL,
        card_last_four TEXT,
        credit_limit REAL NOT NULL,
        billing_day INTEGER NOT NULL,
        card_color TEXT DEFAULT '#4A90E2',
        created_at TEXT NOT NULL,
        FOREIGN KEY (profile_id) REFERENCES profiles (id)
    )''')
    
    # Expenses table
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        note TEXT,
        card_id INTEGER,
        created_at TEXT NOT NULL,
        FOREIGN KEY (profile_id) REFERENCES profiles (id),
        FOREIGN KEY (category_id) REFERENCES categories (id),
        FOREIGN KEY (card_id) REFERENCES credit_cards (id)
    )''')
    
    # Budgets table
    c.execute('''CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_id INTEGER,
        category_id INTEGER,
        amount REAL NOT NULL,
        period TEXT NOT NULL,
        FOREIGN KEY (profile_id) REFERENCES profiles (id),
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )''')
    
    conn.commit()
    conn.close()

def seed_data():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Check if data already exists
    c.execute('SELECT COUNT(*) FROM profiles')
    if c.fetchone()[0] > 0:
        conn.close()
        return
    
    # Insert profiles
    profiles = [
        ('dad', 'Dad'),
        ('mom', 'Mom'),
        ('chaithu', 'Chaithu'),
        ('harshith', 'Harshith'),
        ('common', 'Common')
    ]
    c.executemany('INSERT INTO profiles (name, display_name) VALUES (?, ?)', profiles)
    
    # Insert categories
    categories = [
        ('Rice', 'బియ్యం', '🍚'),
        ('Dal', 'పప్పు', '🫘'),
        ('Oil', 'నూనె', '🛢️'),
        ('Vegetables', 'కూరగాయలు', '🥬'),
        ('Fruits', 'పండ్లు', '🍎'),
        ('Dairy', 'పాల ఉత్పత్తులు', '🥛'),
        ('Snacks', 'స్నాక్స్', '🍿'),
        ('Cleaning', 'శుభ్రపరచడం', '🧹'),
        ('Toiletries', 'సౌందర్య వస్తువులు', '🧴'),
        ('Electricity', 'విద్యుత్', '⚡'),
        ('Water', 'నీరు', '💧'),
        ('Gas', 'గ్యాస్', '🔥'),
        ('Rent/EMI', 'అద్దె/EMI', '🏠'),
        ('Fuel', 'ఇంధనం', '⛽'),
        ('Auto', 'ఆటో', '🛺'),
        ('Bus', 'బస్సు', '🚌'),
        ('Medical', 'వైద్యం', '💊'),
        ('Education', 'విద్య', '📚'),
        ('Movies', 'సినిమాలు', '🎬'),
        ('Dining Out', 'బయట భోజనం', '🍽️'),
        ('Clothing', 'బట్టలు', '👕'),
        ('Electronics', 'ఎలక్ట్రానిక్స్', '📱'),
        ('Gifts', 'బహుమతులు', '🎁'),
        ('Maintenance', 'నిర్వహణ', '🔧'),
        ('Subscriptions', 'చందాలు', '📺'),
        ('Office', 'కార్యాలయం', '💼'),
        ('Travel', 'ప్రయాణం', '✈️'),
        ('Pets', 'పెంపుడు జంతువులు', '🐕'),
        ('Repairs', 'మరమ్మతులు', '🔨'),
        ('Savings', 'పొదుపు', '💰'),
        ('Miscellaneous', 'ఇతరములు', '📦'),
        ('Personal Care', 'వ్యక్తిగత సంరక్షణ', '💅')
    ]
    c.executemany('INSERT INTO categories (name, name_te, icon) VALUES (?, ?, ?)', categories)
    
    conn.commit()
    conn.close()

def get_profiles():
    conn = get_db_connection()
    profiles = conn.execute('SELECT * FROM profiles').fetchall()
    conn.close()
    return [dict(row) for row in profiles]

def get_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return [dict(row) for row in categories]

def add_expense(profile_id, category_id, amount, date, note='', card_id=None):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO expenses (profile_id, category_id, amount, date, note, card_id, created_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (profile_id, category_id, amount, date, note, card_id, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding expense: {e}")
        return False

def get_expenses(profile_id=None, start_date=None, end_date=None, limit=None):
    conn = get_db_connection()
    query = '''SELECT e.id, e.profile_id, p.display_name, e.category_id, c.name, c.name_te, c.icon,
                      e.amount, e.date, e.note, e.card_id, cc.card_name
               FROM expenses e
               JOIN profiles p ON e.profile_id = p.id
               JOIN categories c ON e.category_id = c.id
               LEFT JOIN credit_cards cc ON e.card_id = cc.id
               WHERE 1=1'''
    params = []
    
    if profile_id:
        query += ' AND e.profile_id = ?'
        params.append(profile_id)
    if start_date:
        query += ' AND e.date >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND e.date <= ?'
        params.append(end_date)
    
    query += ' ORDER BY e.date DESC, e.created_at DESC'
    
    if limit:
        query += f' LIMIT {limit}'
        
    runs = conn.execute(query, params).fetchall()
    conn.close()
    
    expenses = []
    for row in runs:
        expenses.append({
            'id': row['id'],
            'profile_id': row['profile_id'],
            'profile_name': row['display_name'],
            'category_id': row['category_id'],
            'category_name': row['name'],
            'category_name_te': row['name_te'],
            'category_icon': row['icon'],
            'amount': row['amount'],
            'date': row['date'],
            'note': row['note'],
            'card_id': row['card_id'],
            'card_name': row['card_name']
        })
    return expenses

def delete_expense(expense_id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def get_credit_cards(profile_id=None):
    conn = get_db_connection()
    query = '''SELECT cc.*, p.display_name 
               FROM credit_cards cc
               JOIN profiles p ON cc.profile_id = p.id
               WHERE 1=1'''
    params = []
    if profile_id:
        query += ' AND cc.profile_id = ?'
        params.append(profile_id)
    
    cards = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in cards]

def add_credit_card(profile_id, card_name, credit_limit, billing_day, card_last_four='', card_color='#4A90E2'):
    try:
        conn = get_db_connection()
        conn.execute('''INSERT INTO credit_cards (profile_id, card_name, card_last_four, credit_limit, 
                                               billing_day, card_color, created_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (profile_id, card_name, card_last_four, credit_limit, billing_day, card_color, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding card: {e}")
        return False

def delete_credit_card(card_id):
    try:
        conn = get_db_connection()
        # Remove card_id from expenses
        conn.execute('UPDATE expenses SET card_id = NULL WHERE card_id = ?', (card_id,))
        # Delete card
        conn.execute('DELETE FROM credit_cards WHERE id = ?', (card_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def get_dashboard_stats(profile_id, period='month'):
    conn = get_db_connection()
    today = datetime.now()
    
    if period == 'week':
        start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    elif period == 'month':
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
    elif period == 'year':
        start_date = today.replace(month=1, day=1).strftime('%Y-%m-%d')
    else:
        start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')

    # Total Spent
    row = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE profile_id = ? AND date >= ?', 
                       (profile_id, start_date)).fetchone()
    total_spent = row[0]
    
    # Category Breakdown
    cat_rows = conn.execute('''SELECT c.name, c.name_te, c.icon, COALESCE(SUM(e.amount), 0) as total
                               FROM categories c
                               LEFT JOIN expenses e ON c.id = e.category_id 
                                  AND e.profile_id = ? AND e.date >= ?
                               GROUP BY c.id, c.name, c.name_te, c.icon
                               HAVING total > 0
                               ORDER BY total DESC''', (profile_id, start_date)).fetchall()
    
    # Weekly Trend
    weekly_data = []
    for i in range(6, -1, -1):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        val = conn.execute('''SELECT COALESCE(SUM(amount), 0) FROM expenses 
                              WHERE profile_id = ? AND date = ?''', (profile_id, date)).fetchone()[0]
        weekly_data.append({'date': date, 'amount': val})
        
    conn.close()
    
    return {
        'total_spent': total_spent,
        'category_breakdown': [dict(r) for r in cat_rows],
        'weekly_trend': weekly_data
    }

def get_family_overview(period='month'):
    conn = get_db_connection()
    today = datetime.now()
    if period == 'week':
        start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    elif period == 'month':
        start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
    else:
        start_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')
        
    # Total Family
    total = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date >= ?', (start_date,)).fetchone()[0]
    
    # By Profile
    prof_rows = conn.execute('''SELECT p.display_name, COALESCE(SUM(e.amount), 0) as total
                                FROM profiles p
                                LEFT JOIN expenses e ON p.id = e.profile_id AND e.date >= ?
                                GROUP BY p.id, p.display_name
                                ORDER BY total DESC''', (start_date,)).fetchall()
                                
    # Top Categories
    cat_rows = conn.execute('''SELECT c.name, c.name_te, COALESCE(SUM(e.amount), 0) as total
                               FROM categories c
                               LEFT JOIN expenses e ON c.id = e.category_id AND e.date >= ?
                               GROUP BY c.id, c.name, c.name_te
                               HAVING total > 0
                               ORDER BY total DESC
                               LIMIT 10''', (start_date,)).fetchall()
    conn.close()
    
    return {
        'total_family': total,
        'profile_spending': [dict(r) for r in prof_rows],
        'top_categories': [dict(r) for r in cat_rows]
    }
