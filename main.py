from flask import Flask, render_template
import sqlite3

connection = sqlite3.connect("inv.db")
cursor = connection.cursor()
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("base.html", loggedIn=False)

def printDb():
    cursor.execute("SELECT * FROM example")
    rows = cursor.fetchall()

    for row in rows:
        print(row)


if __name__ == '__main__':
    pass





