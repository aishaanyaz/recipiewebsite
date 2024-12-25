from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'recipe_app'

mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']
    
    if not username or not email or not password:
        return jsonify({'message': 'All fields are required'}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cur.fetchone()
    
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                (username, email, hashed_password))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    
    if not user or not check_password_hash(user[3], password):  # Password is stored in the 4th column
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'username': user[1]}), 200

if __name__ == '__main__':
    app.run(debug=True)
