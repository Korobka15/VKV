from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
db_path = 'VKVDatabase.db'
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, name, email, password_hash):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, Name, Email, Password_hash FROM Users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(*user_data)
    return None

@app.route('/')
def home():
    return render_template('index.html', user=current_user)

@app.route('/autobus')
def bus():
    return render_template('autobus.html', user=current_user)

@app.route('/forum')
def chat():
    return render_template('forum.html', user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Users WHERE Email = ?", (email,))
        if cursor.fetchone():
            flash('Пользователь с таким email уже существует!', 'danger')
            conn.close()
            return redirect(url_for('register'))
        
        cursor.execute("INSERT INTO Users (Name, Email, Password_hash) VALUES (?, ?, ?)", (name, email, hashed_password))
        conn.commit()
        conn.close()

        flash('Вы успешно зарегистрированы!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, Name, Email, Password_hash FROM Users WHERE Email = ?", (email,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data and bcrypt.check_password_hash(user_data[3], password):
            user = User(*user_data)
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Неверный email или пароль', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
