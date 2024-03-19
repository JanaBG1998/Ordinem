from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3

connection = sqlite3.connect("inv.db")

cursor = connection.cursor()
app = Flask(__name__)
app.config['SECRET_KEY'] = '6d33fa666274b19780e2e1f5a8a1cf56859a17c0a1dec6a2'


@app.route("/")
def main():
    return render_template("base.html", loggedIn=False)

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/register", methods=('GET', 'POST'))
def register():
    user_connection = sqlite3.connect("users.db")
    user_cursor = user_connection.cursor()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['password-repeat']

        if not username:
            flash('Username must be supplied!')
        else:
            if password == repassword:
                user_cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
                user_cursor.execute("DELETE FROM users")
                user_cursor.execute("SELECT * FROM users")
                currentId = len(user_cursor.fetchall()) + 1
                user_cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (++currentId, username, password))
                user_connection.commit()
                user_connection.close()
                return redirect(url_for("home"))

    return render_template("signup.html")


@app.route("/login")
def login():
    return render_template("signin.html")



if __name__ == '__main__':
    pass
    app.run(debug=True)






