import sqlite3
import os
from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

# Helper to setup a dummy database so the app runs
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    c.execute("INSERT INTO users VALUES ('admin', 'secret123')") # Dummy data
    conn.commit()
    conn.close()

# Initialize DB on startup
if not os.path.exists('users.db'):
    init_db()

@app.route('/')
def home():
    # VULNERABILITY 1: Insecure Cookie & Missing Headers
    # ZAP will flag: "Cookie No HttpOnly Flag", "Missing X-Frame-Options"
    resp = make_response("""
    <html>
        <head><title>Vulnerable App</title></head>
        <body>
            <h1>Welcome to the CodeFortress Staging App</h1>
            <p>Use the links below to test features:</p>
            <ul>
                <li><a href="/search">Search Feature (XSS)</a></li>
                <li><a href="/login">Login Feature (SQLi)</a></li>
            </ul>
        </body>
    </html>
    """)
    resp.set_cookie('session_id', '12345-insecure-cookie')
    return resp

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    # VULNERABILITY 2: Reflected XSS
    # We take user input ('q') and put it directly into the HTML without escaping.
    # ZAP Active Scan will inject: <script>alert(1)</script>
    page = """
    <html>
        <body>
            <h2>Search Results</h2>
            <form action="/search" method="get">
                <input type="text" name="q" value="">
                <input type="submit" value="Search">
            </form>
            <p>You searched for: <b>%s</b></p>
        </body>
    </html>
    """ % query
    return page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return """
        <html>
            <body>
                <h2>Login</h2>
                <form action="/login" method="post">
                    Username: <input type="text" name="username"><br>
                    Password: <input type="password" name="password"><br>
                    <input type="submit" value="Login">
                </form>
            </body>
        </html>
        """
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # VULNERABILITY 3: SQL Injection
    # The Active Scan will try injecting: ' OR '1'='1
    query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
    
    try:
        c.execute(query)
        user = c.fetchone()
        conn.close()
        
        if user:
            return "<h1>Login Successful!</h1>"
        else:
            return "<h1>Login Failed</h1>"
    except Exception as e:
        return f"<h1>Database Error: {e}</h1>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)