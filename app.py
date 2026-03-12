import sqlite3
import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = "neuro_secret_key_2026"

# Security: Rate Limiting (Prevents brute force attacks)
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day"])

# --- DATABASE SETUP & AUTO-REPAIR ---
def init_db():
    conn = sqlite3.connect('neuroflow.db')
    cursor = conn.cursor()
    
    # 1. Create Tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, 
         water_cups INTEGER, symptoms TEXT, is_emergency INTEGER, 
         weather_info TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # 2. Force-Create/Update the Doctor (Role-Based Access Control)
    # Password for both is: password123
    hashed_pw = generate_password_hash('password123')
    
    cursor.execute("INSERT OR REPLACE INTO users (id, username, password, role) VALUES (1, ?, ?, ?)", 
                   ('Dr_Shoki', hashed_pw, 'doctor'))
    
    cursor.execute("INSERT OR REPLACE INTO users (id, username, password, role) VALUES (2, ?, ?, ?)", 
                   ('Patient_User', hashed_pw, 'patient'))
    
    conn.commit()
    conn.close()
    print("--- DATABASE SYNCED: Dr_Shoki & Patient_User (password123) are ready! ---")

def get_db():
    conn = sqlite3.connect('neuroflow.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_weather():
    # Placeholder for the presentation - simulates a Weather API call
    return "22°C, Stable Pressure"

# --- ROUTES & BUSINESS LOGIC ---

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        db.close()
        
        # Verify hashed password
        if user and check_password_hash(user['password'], password):
            session.update({
                'user_id': user['id'], 
                'user': user['username'], 
                'role': user['role']
            })
            return redirect(url_for('dashboard'))
        
        flash("Invalid Credentials. Please check your username/password.")
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session: 
        return redirect(url_for('login'))
    
    db = get_db()
    
    # PATIENT ACTION: Add a new medical log (CREATE in CRUD)
    if request.method == 'POST' and session['role'] == 'patient':
        water = request.form.get('water', 0)
        symptoms = request.form.get('symptoms', '')
        
        # CLINICAL LOGIC: Detect high-risk neurological keywords
        emergency_keywords = ['numb', 'vision', 'faint', 'severe', 'dizzy', 'paralysis']
        is_emergency = 1 if any(word in symptoms.lower() for word in emergency_keywords) else 0
        
        weather = get_weather()
        
        db.execute('''INSERT INTO logs (user_id, water_cups, symptoms, is_emergency, weather_info) 
                      VALUES (?,?,?,?,?)''', 
                   (session['user_id'], water, symptoms, is_emergency, weather))
        db.commit()
        flash("Your recovery data has been sent to your doctor.")

    # RBAC LOGIC: Filtering data visibility (READ in CRUD)
    if session['role'] == 'doctor':
        # Doctors see a combined view of all patient data
        logs = db.execute('''SELECT logs.*, users.username 
                             FROM logs JOIN users ON logs.user_id = users.id 
                             ORDER BY timestamp DESC''').fetchall()
    else:
        # Patients only see their own recovery history
        logs = db.execute('SELECT * FROM logs WHERE user_id = ? ORDER BY timestamp DESC', 
                          (session['user_id'],)).fetchall()
    
    db.close()
    return render_template('dashboard.html', logs=logs)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db() # Run auto-repair on startup
    print("NeuroFlow System Running at http://127.0.0.1:5000")
    app.run(debug=True)