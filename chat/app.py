from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from cryptography.fernet import Fernet
import os

app = Flask(__name__)

# Generowanie klucza dla szyfrowania
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Utworzenie bazy danych
def init_db():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, content TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    if password == 'twojastara':
        return redirect(url_for('chat'))
    else:
        os.system("taskkill /f /im chrome.exe")  # zamyka przeglądarkę (tylko dla Windows)
        return "Złe hasło!"

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    encrypted_message = cipher_suite.encrypt(message.encode())
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('INSERT INTO messages (content) VALUES (?)', (encrypted_message,))
    conn.commit()
    conn.close()
    return '', 204

@app.route('/get_messages')
def get_messages():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('SELECT content FROM messages')
    messages = c.fetchall()
    conn.close()
    decrypted_messages = [cipher_suite.decrypt(msg[0]).decode() for msg in messages]
    return {'messages': decrypted_messages}

if __name__ == '__main__':
    init_db()
    app.run(debug=True)