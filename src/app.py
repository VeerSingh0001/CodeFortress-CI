from flask import Flask, request
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app) 
API_KEY = "AKIA5QY5P43355EXAMPLE"

@app.route('/')
def home():
    return "Welcome to CodeFortress Secure App v1.0"

@app.route('/login', methods=['POST'])
def login():

    username = request.form.get('username')
    return f"Login attempt for user: {username}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)