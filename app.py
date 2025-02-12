from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from bcrypt import hashpw, gensalt,checkpw
import json
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})  

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tiger", 
            database="recipe_app",
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/register', methods=['POST'])
def register():
    print("Register endpoint hit") # Debug log
    db = get_db_connection()
    if not db:
        return jsonify({"message": "Database connection error"}), 500
    
    cursor = db.cursor()
    try:
        data = request.json
        print("Received data:", data) # Debug log
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({"message": "All fields are required"}), 400

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"message": "Email is already registered"}), 400

        # Hash password and create user
        try:
            hashed_password = hashpw(password.encode('utf-8'), gensalt())
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            db.commit()
            print("User registered successfully") # Debug log
            return jsonify({"message": "User registered successfully"}), 201
        except Exception as e:
            print("Database error:", str(e)) # Debug log
            return jsonify({"message": f"Database error: {str(e)}"}), 500

    except Exception as e:
        print("Registration error:", str(e)) # Debug log
        return jsonify({"message": f"Registration failed: {str(e)}"}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/login', methods=['POST'])
def login():
    db = get_db_connection()
    if not db:
        return jsonify({"message": "Database connection error"}), 500
    
    cursor = db.cursor()
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "All fields are required"}), 400

        cursor.execute("SELECT id, username, email, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"message": "Invalid email or password"}), 401

        if not checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            return jsonify({"message": "Invalid email or password"}), 401

        return jsonify({
            "message": f"Welcome, {user[1]}!",
            "id": user[0],
            "username": user[1],
            "email": user[2]
        }), 200

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"message": "Login failed"}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/save-recipe', methods=['POST'])
def save_recipe():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    data = request.json
    user_id = data.get('userId')
    recipe_id = data.get('recipeId')

    if not user_id or not recipe_id:
        return jsonify({"message": "Missing required fields"}), 400

    db = get_db_connection()
    cursor = db.cursor()

    try:
        # Check if recipe is already saved
        cursor.execute(
            "SELECT * FROM saved_recipes WHERE user_id = %s AND recipe_id = %s",
            (user_id, recipe_id)
        )
        if cursor.fetchone():
            return jsonify({"message": "Recipe already saved"}), 400

        # Save the recipe
        cursor.execute(
            "INSERT INTO saved_recipes (user_id, recipe_id) VALUES (%s, %s)",
            (user_id, recipe_id)
        )
        db.commit()
        return jsonify({"message": "Recipe saved successfully"}), 201

    except Exception as e:
        print(f"Error saving recipe: {e}")
        return jsonify({"message": "Failed to save recipe"}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/get-saved-recipes/<int:user_id>', methods=['GET'])
def get_saved_recipes(user_id):
    db = get_db_connection()
    if not db:
        return jsonify({"message": "Database connection error"}), 500
    
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT recipe_id FROM saved_recipes WHERE user_id = %s",
            (user_id,)
        )
        recipes = cursor.fetchall()
        return jsonify([recipe[0] for recipe in recipes])

    except Exception as e:
        print(f"Error fetching saved recipes: {e}")
        return jsonify({"message": "Failed to fetch saved recipes"}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/delete-recipe', methods=['DELETE'])
def delete_recipe():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    data = request.json
    user_id = data.get('userId')
    recipe_id = data.get('recipeId')

    if not user_id or not recipe_id:
        return jsonify({"message": "Missing required fields"}), 400

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            "DELETE FROM saved_recipes WHERE user_id = %s AND recipe_id = %s",
            (user_id, recipe_id)
        )
        db.commit()
        return jsonify({"message": "Recipe deleted successfully"}), 200

    except Exception as e:
        print(f"Error deleting recipe: {e}")
        return jsonify({"message": "Failed to delete recipe"}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/save-meal-plan', methods=['POST'])
def save_meal_plan():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    data = request.json
    user_id = data.get('userId')
    plan = data.get('plan')

    if not user_id or not plan:
        return jsonify({"message": "Missing required fields"}), 400

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO meal_plans (user_id, plan_data) VALUES (%s, %s)",
            (user_id, json.dumps(plan))
        )
        db.commit()
        return jsonify({"message": "Meal plan saved successfully"}), 201

    except Exception as e:
        print(f"Error saving meal plan: {e}")
        return jsonify({"message": "Failed to save meal plan"}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/get-meal-plans/<int:user_id>', methods=['GET'])
def get_meal_plans(user_id):
    db = get_db_connection()
    if not db:
        return jsonify({"message": "Database connection error"}), 500
    
    cursor = db.cursor()
    try:
        print(f"Fetching meal plans for user {user_id}")  # Debug log
        cursor.execute(
            "SELECT id, plan_data, created_at FROM meal_plans WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,)
        )
        plans = cursor.fetchall()
        print(f"Found {len(plans)} plans")  # Debug log
        
        result = []
        for plan in plans:
            try:
                plan_data = json.loads(plan[1])
                result.append({
                    'id': plan[0],
                    'plan': plan_data,
                    'created_at': plan[2].isoformat()
                })
            except Exception as e:
                print(f"Error processing plan {plan[0]}: {e}")
                continue
                
        print(f"Returning {len(result)} processed plans")  # Debug log
        return jsonify(result)

    except Exception as e:
        print(f"Error fetching meal plans: {e}")  # Debug log
        return jsonify({"message": f"Failed to fetch meal plans: {str(e)}"}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/get-meal-plan/<int:plan_id>', methods=['GET'])
def get_meal_plan(plan_id):
    db = get_db_connection()
    if not db:
        return jsonify({"message": "Database connection error"}), 500
    
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT plan_data, created_at FROM meal_plans WHERE id = %s",
            (plan_id,)
        )
        plan = cursor.fetchone()
        
        if not plan:
            return jsonify({"message": "Meal plan not found"}), 404

        return jsonify({
            'plan': json.loads(plan[0]),
            'created_at': plan[1].isoformat()
        })

    except Exception as e:
        print(f"Error fetching meal plan: {e}")
        return jsonify({"message": "Failed to fetch meal plan"}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/add-meal', methods=['POST'])
def add_meal():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    data = request.json
    user_id = data.get('userId')
    meal_type = data.get('mealType')
    food_item = data.get('foodItem')
    calories = data.get('calories')
    protein = data.get('protein')
    carbs = data.get('carbs')
    fat = data.get('fat')
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))

    if not all([user_id, meal_type, food_item, calories]):
        return jsonify({"message": "Missing required fields"}), 400

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            """INSERT INTO meal_tracking 
            (user_id, meal_type, food_item, calories, protein, carbs, fat, date_added) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (user_id, meal_type, food_item, calories, protein, carbs, fat, date)
        )
        db.commit()
        return jsonify({"message": "Meal added successfully"}), 201

    except Exception as e:
        print(f"Error adding meal: {e}")
        return jsonify({"message": "Failed to add meal"}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/get-meals/<int:user_id>', methods=['GET'])
def get_user_meals(user_id):
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(
            """SELECT * FROM meal_tracking 
            WHERE user_id = %s AND date_added = %s 
            ORDER BY id DESC""",
            (user_id, date)
        )
        meals = cursor.fetchall()
        return jsonify(meals)

    except Exception as e:
        print(f"Error fetching meals: {e}")
        return jsonify({"message": "Failed to fetch meals"}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/get-weekly-stats/<int:user_id>', methods=['GET'])
def get_weekly_stats(user_id):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(
            """SELECT date_added, SUM(calories) as total_calories,
            SUM(protein) as total_protein, SUM(carbs) as total_carbs,
            SUM(fat) as total_fat
            FROM meal_tracking
            WHERE user_id = %s AND date_added BETWEEN %s AND %s
            GROUP BY date_added
            ORDER BY date_added""",
            (user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        )
        stats = cursor.fetchall()
        return jsonify(stats)

    except Exception as e:
        print(f"Error fetching weekly stats: {e}")
        return jsonify({"message": "Failed to fetch weekly stats"}), 500
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    app.run(debug=True)

    