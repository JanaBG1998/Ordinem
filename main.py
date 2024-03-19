from flask import Flask, render_template
import sqlite3

connection = sqlite3.connect("inv.db")
cursor = connection.cursor()
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("base.html", loggedIn=False)

@app.route("/register")
def register():
    return render_template("signup.html")


@app.route("/login")
def login():
    return render_template("signin.html")

def printDb(db):
    cursor.execute("SELECT * FROM ?", db)
    rows = cursor.fetchall()

    for row in rows:
        print(row)


if __name__ == '__main__':
    pass
    app.run(debug=True)





