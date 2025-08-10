from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

# Create the necessary tables if they don't exist already
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        expected_birth_date TEXT,
        blood_group TEXT,
        address TEXT,
        pincode TEXT,
        contact_number TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_health_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT DEFAULT CURRENT_DATE,           
        heart_rate INTEGER DEFAULT 0,
        pulse_rate INTEGER DEFAULT 0,
        blood_pressure TEXT DEFAULT '0/0',
        footsteps INTEGER DEFAULT 0,
        meditation_time INTEGER DEFAULT 0,
        temperature REAL DEFAULT 0.0,
        sleep_duration INTEGER DEFAULT 0,
        water_intake INTEGER DEFAULT 0,
        calorieintake INTEGER DEFAULT 0,           
        numberofworkout INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS journals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        mood TEXT NOT NULL,
        thoughts TEXT NOT NULL,
        date TEXT DEFAULT CURRENT_DATE,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        doctor_name TEXT,
        date TEXT,
        time TEXT,
        location TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        meal_type TEXT NOT NULL,
        meal_name TEXT NOT NULL,
        meal_date TEXT NOT NULL,
        meal_time TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    conn.commit()
    conn.close()

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    blood_group = data['blood_group']
    address = data['address']
    pincode = data['pincode']
    contact_number = data['contact_number']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO users (username, email, password,
                      blood_group, address, pincode, contact_number) 
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                   (username, email, password, blood_group, 
                    address, pincode, contact_number))

    user_id = cursor.lastrowid  # Get the ID of the newly created user

    conn.commit()
    conn.close()

    return jsonify({
        "message": "User  signed up successfully",
        "user_id": user_id  # Return the user_id in the response
    }), 201

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    
    conn.close()

    if user:
        return jsonify({
            "message": "Login successful",
            "user_id": user['id']
        }), 200
    else:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

# Route to submit daily health data
@app.route('/daily_health_data', methods=['POST'])
def daily_health_data():
    data = request.get_json()

    user_id = data['user_id']
    date = data['date']
    heart_rate = data['heart_rate']
    
    blood_pressure = data['blood_pressure']
    footsteps = data['footsteps']
    meditation_time = data['meditation_time']
    temperature = data['temperature']
    sleep_duration = data['sleep_duration']
    water_intake = data['water_intake']
    calorieintake = data['calorieIntake']
    numberofworkout = data['numberofworkout']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''INSERT INTO daily_health_data (user_id, date, heart_rate, blood_pressure, footsteps, 
                                                          meditation_time, temperature, sleep_duration, water_intake, calorieintake, numberofworkout) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (user_id, date, heart_rate, blood_pressure, footsteps, meditation_time, temperature, 
                        sleep_duration, water_intake, calorieintake, numberofworkout))

        conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback in case of error
        return jsonify({"message": "Error saving data", "error": str(e)}), 500
    finally:
        conn.close()

    return jsonify({
        "message": "Daily health data submitted successfully"
    }), 201

# Route to get daily health data for a user
@app.route('/get_daily_health_data', methods=['GET'])
def get_daily_health_data():
    user_id = request.args.get("user_id")
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM daily_health_data WHERE user_id = ? ORDER BY date DESC', (user_id,))
    data = cursor.fetchall()
    
    conn.close()

    if data:
        health_data = [{
            "date": row["date"],
            "heart_rate": row["heart_rate"],
            "blood_pressure": row["blood_pressure"],
            "footsteps": row["footsteps"],
            "meditation_time": row["meditation_time"],
            "temperature": row["temperature"],
            "sleep_duration": row["sleep_duration"],
            "water_intake": row["water_intake"],
            "calorieintake": row["calorieintake"],
            "numberofworkout": row["numberofworkout"],
        } for row in data]
        
        return jsonify(health_data), 200
    else:
        return jsonify({"message": "No health data found for the user."}), 404

# Route to get all user details
@app.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    
    conn.close()

    if users:
        user_details = [{
            "id": row["id"],
            "username": row["username"],
            "email": row["email"],
            "expected_birth_date": row["expected_birth_date"],
            "blood_group": row["blood_group"],
            "address": row["address"],
            "pincode": row["pincode"],
            "contact_number": row["contact_number"]
        } for row in users]
        
        return jsonify(user_details), 200
    else:
        return jsonify({"message": "No users found."}), 404

# Route to store appointment data
@app.route('/appointments', methods=['POST'])
def store_appointment():
    data = request.get_json()
    user_id = data['user_id']  # This should be dynamic based on the logged-in user
    title = data['title']
    date = data['date']
    time = data['time']
    location = data['location']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO appointments (user_id,doctor_name, date, time, location)
                      VALUES (?, ?, ?, ?, ?)''', (user_id, title , date, time, location))

    conn.commit()
    conn.close()

    return jsonify({"message": "Appointment stored successfully"}), 201

# Route to get appointments for a specific user
@app.route('/getappointments', methods=['GET'])
def get_appointments():
    user_id = request.args.get('user_id')  # Get user_id from query parameters
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM appointments WHERE user_id = ?', (user_id,))
    appointments = cursor.fetchall()
    
    conn.close()

    if appointments:
        appointment_list = [{
            "id": row["id"],
            "title": row["doctor_name"],
            "date": row["date"],
            "time": row["time"],
            "location": row["location"]
        } for row in appointments]
        
        return jsonify(appointment_list), 200
    else:
        return jsonify([]), 200  # Return an empty list if no appointments found

# Route to add a journal entry
@app.route('/journals', methods=['POST'])
def add_journal():
    data = request.get_json()
    user_id = data['user_id']
    title = data['title']
    mood = data['mood']
    thoughts = data['thoughts']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO journals (user_id, title, mood, thoughts) 
                      VALUES (?, ?, ?, ?)''', 
                   (user_id, title, mood, thoughts))

    conn.commit()
    conn.close()

    return jsonify({"message": "Journal entry added successfully"}), 201

# Route to get journal entries for a specific user
@app.route('/journals', methods=['GET'])
def get_journals():
    user_id = request.args.get('user_id')  # Get user_id from query parameters
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM journals WHERE user_id = ?', (user_id,))
    journals = cursor.fetchall()
    
    conn.close()

    if journals:
        journal_list = [{
            "id": row["id"],
            "title": row["title"],
            "mood": row["mood"],
            "thoughts": row["thoughts"],
            "date": row["date"]
        } for row in journals]
        
        return jsonify(journal_list), 200
    else:
        return jsonify([]), 200  # Return an empty list if no journals found

# Route to add a meal
@app.route('/meals', methods=['POST'])
def add_meal():
    data = request.get_json()
    user_id = data['user_id']
    meal_type = data['meal_type']
    meal_name = data['meal_name']
    meal_date = data['meal_date']
    meal_time = data['meal_time']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO meals (user_id, meal_type, meal_name, meal_date, meal_time) 
                      VALUES (?, ?, ?, ?, ?)''', 
                   (user_id, meal_type, meal_name, meal_date, meal_time))

    conn.commit()
    conn.close()

    return jsonify({"message": "Meal added successfully"}), 201

# Route to get meals for a specific user
@app.route('/getmeals', methods=['GET'])
def get_meals():
    user_id = request.args.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM meals WHERE user_id = ?', (user_id,))
    meals = cursor.fetchall()
    
    conn.close()

    if meals:
        meal_list = [{
            "id": row["id"],
            "meal_type": row["meal_type"],
            "meal_name": row["meal_name"],
            "meal_date": row["meal_date"],
            "meal_time": row["meal_time"]
        } for row in meals]
        
        return jsonify(meal_list), 200
    else:
        return jsonify([]), 200  # Return an empty list if no meals found

if __name__ == '__main__':
    create_tables()  # Ensure the tables are created when the app starts
    app.run(debug=True)