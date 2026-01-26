from flask import Flask, request
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app) 
aws_access_key_id="AKIAIOSFODNN7EXAMPLE"
aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

@app.route('/')
def home():
    return "Welcome to CodeFortress Secure App v1.0"

@app.route('/login', methods=['POST'])
def login():

    username = request.form.get('username')
    return f"Login attempt for user: {username}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)