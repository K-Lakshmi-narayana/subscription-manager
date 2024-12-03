from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize database
def init_db():
    with sqlite3.connect('instance/database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS CUSTOMER (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            pan TEXT UNIQUE NOT NULL
        );''')
        conn.execute('''CREATE TABLE IF NOT EXISTS PRODUCT (
            product_name TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            annual_subscription_cost FLOAT NOT NULL
        );''')
        conn.execute('''CREATE TABLE IF NOT EXISTS SUBSCRIPTION (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            product_name TEXT,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            num_users INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
            FOREIGN KEY (product_name) REFERENCES PRODUCT(product_name)
        );''')
        conn.commit()
        print("Tables initialized!")

init_db()

@app.route('/customers', methods=['GET', 'POST'])
def manage_customers():
    if request.method == 'POST':
        data = request.json
        customer_id, name, pan = data['customer_id'], data['name'], data['pan']
        with sqlite3.connect('instance/database.db') as conn:
            try:
                conn.execute("INSERT INTO CUSTOMER (customer_id, name, pan) VALUES (?, ?, ?)", (customer_id, name, pan))
                conn.commit()
                return jsonify({'message': 'Customer added successfully!'}), 201
            except sqlite3.IntegrityError as e:
                return jsonify({'error': str(e)}), 400
    with sqlite3.connect('instance/database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM CUSTOMER")
        customers = cur.fetchall()
    return jsonify(customers)

@app.route('/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'POST':
        data = request.json
        product_name, description, annual_subscription_cost = data['product_name'], data['description'], data['annual_subscription_cost']
        with sqlite3.connect('instance/database.db') as conn:
            try:
                conn.execute("INSERT INTO PRODUCT (product_name, description, annual_subscription_cost) VALUES (?, ?, ?)",
                             (product_name, description, annual_subscription_cost))
                conn.commit()
                return jsonify({'message': 'Product added successfully!'}), 201
            except sqlite3.IntegrityError as e:
                return jsonify({'error': str(e)}), 400
    with sqlite3.connect('instance/database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM PRODUCT")
        products = cur.fetchall()
    return jsonify(products)

@app.route('/subscriptions', methods=['GET', 'POST'])
def manage_subscriptions():
    if request.method == 'POST':
        data = request.json
        customer_id, product_name, start_date, end_date, num_users = (
            data['customer_id'], data['product_name'], data['start_date'], data['end_date'], data['num_users']
        )
        with sqlite3.connect('instance/database.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM SUBSCRIPTION WHERE customer_id = ? AND product_name = ? AND end_date >= ?',
                        (customer_id, product_name, datetime.now().date()))
            active_subscription = cur.fetchone()
            if active_subscription:
                return jsonify({'error': 'Active subscription already exists for this customer-product combination.'}), 400
            cur.execute('''INSERT INTO SUBSCRIPTION (customer_id, product_name, start_date, end_date, num_users) 
                           VALUES (?, ?, ?, ?, ?)''', (customer_id, product_name, start_date, end_date, num_users))
            conn.commit()
        return jsonify({'message': 'Subscription added successfully!'}), 201
    with sqlite3.connect('instance/database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM SUBSCRIPTION')
        subscriptions = cur.fetchall()
    return jsonify(subscriptions)

@app.route('/revenue_report', methods=['GET'])
def revenue_report():
    with sqlite3.connect('instance/database.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT SUM(p.annual_subscription_cost * s.num_users) AS revenue
            FROM SUBSCRIPTION s
            JOIN PRODUCT p ON s.product_name = p.product_name
            WHERE s.end_date >= DATE('now')
        ''')
        revenue = cur.fetchone()[0] or 0
    return jsonify({'revenue': revenue})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
