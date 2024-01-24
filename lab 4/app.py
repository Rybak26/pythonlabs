import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'bilka'


class UserHandler:
    def __init__(self, file_path='clients.json'):
        self.file_path = file_path
        self.reload_users()

    def load_users(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_users(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.users, f, indent=4)

    def user_exists(self, username):
        return username in self.users

    def verify_credentials(self, username, password):
        return self.user_exists(username) and self.users[username]['password'] == password

    def change_user_password(self, username, new_password):
        if self.user_exists(username):
            self.users[username]['password'] = new_password
            self.save_users()
            self.reload_users()

    def reload_users(self):
        self.users = self.load_users()


class CookieHandler:
    def __init__(self):
        self.user_cookies = {}

    def add_cookie(self, key, value, expiry):
        self.user_cookies[key] = {"value": value, "expiry": expiry, "creation_time": str(datetime.datetime.now())}

    def delete_cookie(self, key):
        if key in self.user_cookies:
            self.user_cookies.pop(key)

    def delete_all_cookies(self):
        self.user_cookies.clear()

    def get_user_cookies(self):
        cookies_list = []
        for key, cookie in self.user_cookies.items():
            expiry_time = datetime.datetime.strptime(cookie['creation_time'], '%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(seconds=cookie['expiry'])
            cookies_list.append({
                'key': key,
                'value': cookie['value'],
                'expiry': expiry_time,
                'creation_time': cookie['creation_time']
            })
        return cookies_list


user_handler = UserHandler()
cookie_handler = CookieHandler()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if user_handler.verify_credentials(username, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('info'))
        else:
            flash('Invalid username or password', 'danger')
            print(f"Invalid login attempt: username={username}, password={password}")

    return render_template('login.html')


@app.route('/info')
def info():
    username = session.get('username', None)
    if username:
        user_info = user_handler.users.get(username, None)
        if user_info:
            cookies = cookie_handler.get_user_cookies()
            return render_template('info.html', user_info=user_info, cookies=cookies)
    return redirect(url_for('login'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    flash('Logout successful!', 'success')
    cookie_handler.user_cookies.clear()
    return redirect(url_for('login'))


@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    username = session.get('username', None)
    if username:
        key = request.form['cookie_key']
        value = request.form['cookie_value']
        expiry = int(request.form['cookie_expiry'])
        cookie_handler.add_cookie(key, value, expiry)
        flash('Cookie added successfully!', 'success')
    return redirect(url_for('info'))


@app.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    username = session.get('username', None)
    if username:
        key = request.form['delete_cookie_key']
        cookie_handler.delete_cookie(key)
        flash('Cookie deleted successfully!', 'success')
    return redirect(url_for('info'))


@app.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    username = session.get('username', None)
    if username:
        cookie_handler.delete_all_cookies()
        flash('All cookies deleted successfully!', 'success')
    return redirect(url_for('info'))


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    username = session.get('username', None)
    if username:
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            if new_password:
                user_handler.change_user_password(username, new_password)
                flash('Password changed successfully!', 'success')
    return redirect(url_for('info'))


if __name__ == '__main__':
    app.run(debug=True)
