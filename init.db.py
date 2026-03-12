import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    conn = sqlite3.connect('neuroflow.db')
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)''')
    
    # Medical Logs Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, 
         water_cups INTEGER, symptoms TEXT, is_emergency INTEGER, 
         weather_info TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # Default Accounts (Password: password123)
    users = [
        ('Dr_Shoki', generate_password_hash('password123'), 'doctor'),
        ('Patient_User', generate_password_hash('password123'), 'patient')
    ]
    for u in users:
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", u)
        except sqlite3.IntegrityError: pass
        
    conn.commit()
    conn.close()
    print("Database ready! Use 'Dr_Shoki' to log in as doctor.")

if __name__ == "__main__":
    init_db()