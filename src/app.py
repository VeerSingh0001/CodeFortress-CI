import os
import sqlite3
import hashlib
from flask import Flask, request
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app) 

# VULNERABILITY 1: Hardcoded Secret (SonarQube should flag this as a Security Hotspot)
SECRET_KEY = "admin123"

@app.route('/')
def home():
    return "Welcome to the Vulnerable App!"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # VULNERABILITY 2: Weak Cryptography (MD5 is broken)
    # SonarQube Rule: "MD5 and SHA-1 should not be used"
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # VULNERABILITY 3: SQL Injection
    # SonarQube Rule: "Database queries should not be vulnerable to injection attacks"
    # We are using string formatting instead of parameterized queries (?)
    query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, hashed_password)
    c.execute(query)
    
    user = c.fetchone()
    conn.close()
    
    if user:
        return "Login Successful"
    else:
        return "Login Failed"

@app.route('/hello')
def hello():
    name = request.args.get('name')
    # VULNERABILITY 4: Reflected XSS (Cross-Site Scripting)
    # SonarQube Rule: "User input should be sanitized before being returned"
    return "Hello, %s" % name

if __name__ == '__main__':
    # VULNERABILITY 5: Debug Mode Enabled
    # SonarQube Rule: "Debug mode should not be enabled in production"
    app.run(debug=True)