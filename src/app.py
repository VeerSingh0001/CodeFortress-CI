import os
import sqlite3
import hashlib
from flask import Flask, request, escape, make_response
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default-key-for-dev')

@app.route('/')
def home():
    # VULNERABILITY 1: Insecure Cookie
    # We are setting a cookie without 'HttpOnly' (Javascript can read it) 
    # and without 'Secure' (Sent over HTTP).
    # ZAP Alert: "Cookie No HttpOnly Flag" / "Cookie Without Secure Flag"
    resp = make_response("Welcome to the Vulnerable DAST App!")
    resp.set_cookie('session_token', 'sensitive_admin_data_123')
    
    # VULNERABILITY 2: Server Leaking Information
    # We are pretending to be an old PHP server.
    # ZAP Alert: "Server Leaks Information via 'X-Powered-By'"
    resp.headers['X-Powered-By'] = 'PHP/5.6.0 (Vulnerable)'
    
    return resp

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    c.execute(query, (username, hashed_password))
    user = c.fetchone()
    conn.close()
    
    if user:
        return "Login Successful"
    else:
        return "Login Failed"

@app.route('/hello')
def hello():
    name = request.args.get('name')
    safe_name = escape(name)
    return "Hello, %s" % safe_name

if __name__ == '__main__':
    # Run on 0.0.0.0 so Docker can see it
    app.run(debug=False, host='0.0.0.0', port=5000)
