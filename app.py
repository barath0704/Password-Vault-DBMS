from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'cookie dough'  # CHANGE THIS IN PRODUCTION

# MySQL configuration
app.config['MYSQL_HOST'] = 'db4free.net'
app.config['MYSQL_USER'] = 'barathuser'
app.config['MYSQL_PASSWORD'] = 'barath2004'
app.config['MYSQL_DB'] = 'password_vault'

mysql = MySQL(app)

# ---------------------- Encryption Key (Persistent) ----------------------
KEY_FILE = "secret.key"

def load_or_create_fernet_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

fernet_key = load_or_create_fernet_key()
cipher_suite = Fernet(fernet_key)

# ---------------------- Admin Login ----------------------
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials')
    return render_template('admin_login.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/admin/users')
def admin_users():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('admin_users.html', users=users)

@app.route('/admin/credentials')
def admin_credentials():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    site_name = request.args.get('site_name', '').strip()
    site_username = request.args.get('site_username', '').strip()
    user_id = request.args.get('user_id', '').strip()

    query = "SELECT id, user_id, site_name, site_username, site_password_encrypted, notes FROM credentials WHERE 1=1"
    params = []

    if site_name:
        query += " AND site_name LIKE %s"
        params.append(f"%{site_name}%")
    if site_username:
        query += " AND site_username LIKE %s"
        params.append(f"%{site_username}%")
    if user_id:
        query += " AND user_id = %s"
        params.append(user_id)

    cur = mysql.connection.cursor()
    cur.execute(query, params)
    credentials = cur.fetchall()
    cur.close()
    return render_template('admin_credentials.html', credentials=credentials)

# ---------------------- User Registration ----------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        password_hash = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        existing = cur.fetchone()

        if existing:
            flash("Username already exists.")
            return redirect(url_for('register'))

        cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        mysql.connection.commit()
        cur.close()
        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

# ---------------------- User Login ----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password_input):
            session['user_id'] = user[0]
            session['username'] = username
            flash("Logged in successfully.")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))

    return render_template('login.html')

# ---------------------- Logout ----------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('login'))

# ---------------------- Home Page ----------------------
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, site_name, site_username, site_password_encrypted, notes
        FROM credentials
        WHERE user_id = %s
    """, (session['user_id'],))
    credentials = cur.fetchall()
    cur.close()

    decrypted_credentials = []
    for row in credentials:
        try:
            decrypted_password = cipher_suite.decrypt(row[3].encode()).decode()
        except Exception:
            decrypted_password = "[DECRYPTION ERROR]"
        decrypted_credentials.append((row[0], row[1], row[2], decrypted_password, row[4]))

    return render_template('index.html', credentials=decrypted_credentials)

# ---------------------- Add Credential ----------------------
@app.route('/add', methods=['POST'])
def add_credential():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    site_name = request.form['site_name']
    site_username = request.form['site_username']
    site_password = request.form['site_password']
    notes = request.form['notes']

    encrypted_password = cipher_suite.encrypt(site_password.encode()).decode()

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO credentials (user_id, site_name, site_username, site_password_encrypted, notes)
        VALUES (%s, %s, %s, %s, %s)
    """, (session['user_id'], site_name, site_username, encrypted_password, notes))
    mysql.connection.commit()
    cur.close()

    flash("Credential added successfully.")
    return redirect(url_for('home'))

# ---------------------- Delete Credential ----------------------
@app.route('/delete/<int:cred_id>')
def delete_credential(cred_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM credentials WHERE id = %s AND user_id = %s", (cred_id, session['user_id']))
    mysql.connection.commit()
    cur.close()

    flash("Credential deleted.")
    return redirect(url_for('home'))

# ---------------------- Update Credential ----------------------
@app.route('/update/<int:cred_id>', methods=['POST'])
def update_credential(cred_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    site_name = request.form['site_name']
    site_username = request.form['site_username']
    site_password = request.form['site_password']
    notes = request.form['notes']

    encrypted_password = cipher_suite.encrypt(site_password.encode()).decode()

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE credentials
        SET site_name = %s, site_username = %s, site_password_encrypted = %s, notes = %s
        WHERE id = %s AND user_id = %s
    """, (site_name, site_username, encrypted_password, notes, cred_id, session['user_id']))
    mysql.connection.commit()
    cur.close()

    flash("Credential updated successfully.")
    return redirect(url_for('home'))

# ---------------------- Run App ----------------------
if __name__ == "__main__":
    app.run(debug=True)
