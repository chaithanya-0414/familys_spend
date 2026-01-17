from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import os
import csv
from io import StringIO

app = Flask(__name__, static_folder='.')
CORS(app)

DATABASE = 'data.db'

# Database initialization
def init_db():
    conn = sqlite3.connect(DATABASE)
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

# Seed initial data
def seed_data():
    conn = sqlite3.connect(DATABASE)
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
    
    # Insert categories with Telugu translations
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
    
    # No sample expenses - start with clean database
    
    conn.commit()
    conn.close()

# API Routes
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT id, name, display_name FROM profiles')
    profiles = [{'id': row[0], 'name': row[1], 'display_name': row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify(profiles)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT id, name, name_te, icon FROM categories')
    categories = [{'id': row[0], 'name': row[1], 'name_te': row[2], 'icon': row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify(categories)

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    profile_id = request.args.get('profile_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    query = '''SELECT e.id, e.profile_id, p.display_name, e.category_id, c.name, c.name_te, c.icon,
                      e.amount, e.date, e.note, e.created_at
               FROM expenses e
               JOIN profiles p ON e.profile_id = p.id
               JOIN categories c ON e.category_id = c.id
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
    
    c.execute(query, params)
    expenses = [{
        'id': row[0],
        'profile_id': row[1],
        'profile_name': row[2],
        'category_id': row[3],
        'category_name': row[4],
        'category_name_te': row[5],
        'category_icon': row[6],
        'amount': row[7],
        'date': row[8],
        'note': row[9],
        'created_at': row[10]
    } for row in c.fetchall()]
    
    conn.close()
    return jsonify(expenses)

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    try:
        data = request.json
        print(f"Received expense data: {data}")
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        # Validate required fields
        if 'profile_id' not in data or 'category_id' not in data or 'amount' not in data or 'date' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        c.execute('''INSERT INTO expenses (profile_id, category_id, amount, date, note, card_id, created_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (data['profile_id'], data['category_id'], data['amount'], 
                   data['date'], data.get('note', ''), data.get('card_id'), datetime.now().isoformat()))
        
        expense_id = c.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'id': expense_id, 'message': 'Expense added successfully'}), 201
    except Exception as e:
        print(f"Error adding expense: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Expense deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting expense: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/<int:profile_id>', methods=['GET'])
def get_dashboard(profile_id):
    period = request.args.get('period', 'month')  # week, month, year
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Calculate date range
    today = datetime.now()
    start_date = today.strftime('%Y-%m-%d') # Default fallback
    
    if period == 'week':
        start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    elif period == 'month':
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
    elif period == 'year':
        start_date = today.replace(month=1, day=1).strftime('%Y-%m-%d')
    else:
        start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        
    # Total spent
    c.execute('''SELECT COALESCE(SUM(amount), 0) FROM expenses 
                 WHERE profile_id = ? AND date >= ?''', (profile_id, start_date))
    total_spent = c.fetchone()[0]
    
    # Category breakdown
    c.execute('''SELECT c.name, c.name_te, c.icon, COALESCE(SUM(e.amount), 0) as total
                 FROM categories c
                 LEFT JOIN expenses e ON c.id = e.category_id 
                    AND e.profile_id = ? AND e.date >= ?
                 GROUP BY c.id, c.name, c.name_te, c.icon
                 HAVING total > 0
                 ORDER BY total DESC''', (profile_id, start_date))
    
    category_breakdown = [{
        'category': row[0],
        'category_te': row[1],
        'icon': row[2],
        'amount': row[3]
    } for row in c.fetchall()]
    
    # Top 3 categories
    top_categories = category_breakdown[:3]
    
    # Weekly trend (last 7 days)
    weekly_data = []
    for i in range(6, -1, -1):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        c.execute('''SELECT COALESCE(SUM(amount), 0) FROM expenses 
                     WHERE profile_id = ? AND date = ?''', (profile_id, date))
        amount = c.fetchone()[0]
        weekly_data.append({'date': date, 'amount': amount})
    
    conn.close()
    
    return jsonify({
        'total_spent': total_spent,
        'category_breakdown': category_breakdown,
        'top_categories': top_categories,
        'weekly_trend': weekly_data
    })

@app.route('/api/family-overview', methods=['GET'])
def get_family_overview():
    period = request.args.get('period', 'month')
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    today = datetime.now()
    if period == 'week':
        start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    elif period == 'month':
        start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
    else:
        start_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')
    
    # Total family spending
    c.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date >= ?', (start_date,))
    total_family = c.fetchone()[0]
    
    # Spending by profile
    c.execute('''SELECT p.display_name, COALESCE(SUM(e.amount), 0) as total
                 FROM profiles p
                 LEFT JOIN expenses e ON p.id = e.profile_id AND e.date >= ?
                 GROUP BY p.id, p.display_name
                 ORDER BY total DESC''', (start_date,))
    
    profile_spending = [{'profile': row[0], 'amount': row[1]} for row in c.fetchall()]
    
    # Category breakdown for entire family
    c.execute('''SELECT c.name, c.name_te, COALESCE(SUM(e.amount), 0) as total
                 FROM categories c
                 LEFT JOIN expenses e ON c.id = e.category_id AND e.date >= ?
                 GROUP BY c.id, c.name, c.name_te
                 HAVING total > 0
                 ORDER BY total DESC
                 LIMIT 10''', (start_date,))
    
    top_categories = [{'category': row[0], 'category_te': row[1], 'amount': row[2]} for row in c.fetchall()]
    
    conn.close()
    
    return jsonify({
        'total_family': total_family,
        'profile_spending': profile_spending,
        'top_categories': top_categories
    })

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    profile_id = request.args.get('profile_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    query = '''SELECT e.date, p.display_name, c.name, e.amount, e.note
               FROM expenses e
               JOIN profiles p ON e.profile_id = p.id
               JOIN categories c ON e.category_id = c.id
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
    
    query += ' ORDER BY e.date DESC'
    
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Profile', 'Category', 'Amount', 'Note'])
    writer.writerows(rows)
    
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': f'attachment; filename=expenses_{datetime.now().strftime("%Y%m%d")}.csv'
    }

# Credit Card API Routes
@app.route('/api/credit-cards', methods=['GET'])
def get_all_credit_cards():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''SELECT cc.id, cc.profile_id, p.display_name, cc.card_name, cc.card_last_four, 
                        cc.credit_limit, cc.billing_day, cc.card_color, cc.created_at
                 FROM credit_cards cc
                 JOIN profiles p ON cc.profile_id = p.id
                 ORDER BY cc.created_at DESC''')
    
    cards = [{
        'id': row[0],
        'profile_id': row[1],
        'profile_name': row[2],
        'card_name': row[3],
        'card_last_four': row[4],
        'credit_limit': row[5],
        'billing_day': row[6],
        'card_color': row[7],
        'created_at': row[8]
    } for row in c.fetchall()]
    
    conn.close()
    return jsonify(cards)

@app.route('/api/credit-cards/<int:profile_id>', methods=['GET'])
def get_profile_credit_cards(profile_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''SELECT id, profile_id, card_name, card_last_four, credit_limit, 
                        billing_day, card_color, created_at
                 FROM credit_cards
                 WHERE profile_id = ?
                 ORDER BY created_at DESC''', (profile_id,))
    
    cards = [{
        'id': row[0],
        'profile_id': row[1],
        'card_name': row[2],
        'card_last_four': row[3],
        'credit_limit': row[4],
        'billing_day': row[5],
        'card_color': row[6],
        'created_at': row[7]
    } for row in c.fetchall()]
    
    conn.close()
    return jsonify(cards)

@app.route('/api/credit-cards', methods=['POST'])
def add_credit_card():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('''INSERT INTO credit_cards (profile_id, card_name, card_last_four, credit_limit, 
                                           billing_day, card_color, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (data['profile_id'], data['card_name'], data.get('card_last_four', ''), 
               data['credit_limit'], data['billing_day'], data.get('card_color', '#4A90E2'),
               datetime.now().isoformat()))
    
    card_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': card_id, 'message': 'Credit card added successfully'}), 201

@app.route('/api/credit-cards/<int:card_id>', methods=['PUT'])
def update_credit_card(card_id):
    data = request.json
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('''UPDATE credit_cards 
                 SET card_name = ?, card_last_four = ?, credit_limit = ?, 
                     billing_day = ?, card_color = ?
                 WHERE id = ?''',
              (data['card_name'], data.get('card_last_four', ''), data['credit_limit'],
               data['billing_day'], data.get('card_color', '#4A90E2'), card_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Credit card updated successfully'}), 200

@app.route('/api/credit-cards/<int:card_id>', methods=['DELETE'])
def delete_credit_card(card_id):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        # Remove card_id from expenses (set to NULL)
        c.execute('UPDATE expenses SET card_id = NULL WHERE card_id = ?', (card_id,))
        
        # Delete the card
        c.execute('DELETE FROM credit_cards WHERE id = ?', (card_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Credit card deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting credit card: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/credit-cards/<int:card_id>/dashboard', methods=['GET'])
def get_card_dashboard(card_id):
    period = request.args.get('period', 'month')
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Get card details
    c.execute('''SELECT card_name, card_last_four, credit_limit, billing_day, card_color
                 FROM credit_cards WHERE id = ?''', (card_id,))
    card_row = c.fetchone()
    
    if not card_row:
        conn.close()
        return jsonify({'error': 'Card not found'}), 404
    
    card_info = {
        'card_name': card_row[0],
        'card_last_four': card_row[1],
        'credit_limit': card_row[2],
        'billing_day': card_row[3],
        'card_color': card_row[4]
    }
    
    # Calculate date range based on billing cycle
    today = datetime.now()
    current_month = today.month
    current_year = today.year
    billing_day = card_info['billing_day']
    
    if today.day >= billing_day:
        # Current billing cycle
        cycle_start = datetime(current_year, current_month, billing_day)
        if current_month == 12:
            cycle_end = datetime(current_year + 1, 1, billing_day) - timedelta(days=1)
        else:
            cycle_end = datetime(current_year, current_month + 1, billing_day) - timedelta(days=1)
    else:
        # Previous billing cycle
        if current_month == 1:
            cycle_start = datetime(current_year - 1, 12, billing_day)
        else:
            cycle_start = datetime(current_year, current_month - 1, billing_day)
        cycle_end = datetime(current_year, current_month, billing_day) - timedelta(days=1)
    
    # Total spent in current billing cycle
    c.execute('''SELECT COALESCE(SUM(amount), 0) FROM expenses 
                 WHERE card_id = ? AND date >= ? AND date <= ?''',
              (card_id, cycle_start.strftime('%Y-%m-%d'), cycle_end.strftime('%Y-%m-%d')))
    total_spent = c.fetchone()[0]
    
    # Available balance
    available_balance = card_info['credit_limit'] - total_spent
    utilization = (total_spent / card_info['credit_limit'] * 100) if card_info['credit_limit'] > 0 else 0
    
    # Category breakdown for this card
    c.execute('''SELECT c.name, c.name_te, c.icon, COALESCE(SUM(e.amount), 0) as total
                 FROM categories c
                 LEFT JOIN expenses e ON c.id = e.category_id 
                    AND e.card_id = ? AND e.date >= ? AND e.date <= ?
                 GROUP BY c.id, c.name, c.name_te, c.icon
                 HAVING total > 0
                 ORDER BY total DESC
                 LIMIT 5''', (card_id, cycle_start.strftime('%Y-%m-%d'), cycle_end.strftime('%Y-%m-%d')))
    
    category_breakdown = [{
        'category': row[0],
        'category_te': row[1],
        'icon': row[2],
        'amount': row[3]
    } for row in c.fetchall()]
    
    # Recent transactions
    c.execute('''SELECT e.id, e.amount, e.date, e.note, c.name, c.icon
                 FROM expenses e
                 JOIN categories c ON e.category_id = c.id
                 WHERE e.card_id = ?
                 ORDER BY e.date DESC, e.created_at DESC
                 LIMIT 10''', (card_id,))
    
    recent_transactions = [{
        'id': row[0],
        'amount': row[1],
        'date': row[2],
        'note': row[3],
        'category': row[4],
        'icon': row[5]
    } for row in c.fetchall()]
    
    conn.close()
    
    return jsonify({
        'card_info': card_info,
        'total_spent': total_spent,
        'available_balance': available_balance,
        'utilization': round(utilization, 1),
        'cycle_start': cycle_start.strftime('%Y-%m-%d'),
        'cycle_end': cycle_end.strftime('%Y-%m-%d'),
        'category_breakdown': category_breakdown,
        'recent_transactions': recent_transactions
    })

@app.route('/api/budgets', methods=['GET'])
def get_budgets():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''SELECT b.id, b.profile_id, p.display_name, b.category_id, c.name, b.amount, b.period
                 FROM budgets b
                 LEFT JOIN profiles p ON b.profile_id = p.id
                 LEFT JOIN categories c ON b.category_id = c.id''')
    
    budgets = [{
        'id': row[0],
        'profile_id': row[1],
        'profile_name': row[2],
        'category_id': row[3],
        'category_name': row[4],
        'amount': row[5],
        'period': row[6]
    } for row in c.fetchall()]
    
    conn.close()
    return jsonify(budgets)

@app.route('/api/budgets', methods=['POST'])
def set_budget():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Check if budget exists
    c.execute('''SELECT id FROM budgets 
                 WHERE profile_id = ? AND category_id = ? AND period = ?''',
              (data.get('profile_id'), data.get('category_id'), data['period']))
    
    existing = c.fetchone()
    
    if existing:
        c.execute('''UPDATE budgets SET amount = ? 
                     WHERE id = ?''', (data['amount'], existing[0]))
    else:
        c.execute('''INSERT INTO budgets (profile_id, category_id, amount, period)
                     VALUES (?, ?, ?, ?)''',
                  (data.get('profile_id'), data.get('category_id'), 
                   data['amount'], data['period']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Budget set successfully'}), 201

if __name__ == '__main__':
    init_db()
    seed_data()
    print("🚀 FamilySpend is running at http://localhost:5000")
    print("📱 Open in mobile view for best experience")
    app.run(debug=True, host='0.0.0.0', port=5000)
