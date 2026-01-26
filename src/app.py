import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Vulnerable App!"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # ❌ VULNERABILITY: SQL Injection
    # We are using string formatting (%) to build the query.
    # An attacker can input: admin' OR '1'='1
    query = "SELECT * FROM users WHERE username = '%s'" % username
    
    # Execute the raw string
    c.execute(query)
    
    user = c.fetchone()
    conn.close()
    
    if user:
        return "Login Successful"
    else:
        return "Login Failed"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)