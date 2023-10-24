from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Using SQLite for the example
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Sample user data for demonstration
users = {
    'john_doe': {'password': 'password'}
}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Sign up route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    # Add logic to store user data in the database
    return jsonify({'message': 'User created successfully!'})

# Login route
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic auth="Login required!"'}), 401

    username = auth.username
    password = auth.password

    if users.get(username) and users[username]['password'] == password:
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return jsonify({'message': 'Invalid credentials'}), 401

# Dashboard route
@app.route('/dashboard')
def dashboard():
    # Add JWT token verification logic here
    return render_template('dashboard.html')

# Contact route
@app.route('/contact', methods=['POST'])
def contact():
    # Add JWT token verification logic here
    data = request.get_json()
    # Add logic to store the contact form data in the database
    return jsonify({'message': 'Message received!'})

if __name__ == '__main__':
    app.run(debug=True)
