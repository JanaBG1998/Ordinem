from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import *
from flask_bcrypt import Bcrypt
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from collections import Counter
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '6d33fa666274b19780e2e1f5a8a1cf56859a17c0a1dec6a2'

# Tells flask-sqlalchemy what database to connect to
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
    email = db.Column(db.String(250),
                      nullable=False)
    userType = db.Column(db.String(250),
                         nullable=False)


# Initialize app with extension
db.init_app(app)
# Create database within app context

with app.app_context():
    db.create_all()


def getDashboardMetrics():
    conn = sqlite3.connect('instance/inventar.db')
    cursor = conn.cursor()

    # count items
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    counter = Counter(item[1] for item in items)

    # find most common item
    most_common_item = counter.most_common(1)[0][0]

    # find item to order
    cursor.execute("SELECT name FROM items ORDER BY amount ASC LIMIT 1")
    item_with_lowest_amount = cursor.fetchone()[0]

    # get rooms
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()

    # get current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    two_weeks_later = (datetime.now() + timedelta(weeks=2)).strftime('%Y-%m-%d')

    # SQL-Abfrage ausführen, um das Element mit dem nächsten Ablaufdatum innerhalb der nächsten 2 Wochen oder bereits überschritten abzurufen
    cursor.execute(
        "SELECT name, expiry_date FROM items WHERE expiry_date IS NOT NULL AND (expiry_date <= ? OR expiry_date <= ?) ORDER BY expiry_date ASC LIMIT 1",
        (current_date, two_weeks_later))
    item_nearest_expiration = cursor.fetchone()
    return [len(items), most_common_item, item_with_lowest_amount, len(rooms), item_nearest_expiration]

def getRooms():
    conn = sqlite3.connect('instance/inventar.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM rooms")
    return cursor.fetchall()

def getItems():
    conn = sqlite3.connect('instance/inventar.db')
    cursor = conn.cursor()

    cursor.execute("SELECT items.id, items.name AS item_name, items.amount, items.price, items.weight, items.color, items.expiry_date, rooms.name AS room_name FROM items INNER JOIN rooms ON items.room_id = rooms.id")
    return cursor.fetchall()

def getItem(id):
    conn = sqlite3.connect('instance/inventar.db')
    cursor = conn.cursor()

    cursor.execute("SELECT items.id, items.name AS item_name, items.amount, items.price, items.weight, items.color, items.expiry_date, rooms.name AS room_name, items.room_id AS room_id FROM items INNER JOIN rooms ON items.room_id = rooms.id WHERE items.id = ?", id)
    return cursor.fetchone()

@app.route("/")
def main():
    return render_template("base.html")


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['password-repeat']
        mail = request.form['mail']
        userType = request.form['btnradio']

        if not username or not password or not repassword:
            flash('Username and password must be supplied!')
        else:
            pass
        if password == repassword:
            if not Users.query.filter_by(
                    username=request.form.get("username")).first():
                user = Users(username=username,
                             password=bcrypt.generate_password_hash(password).decode('utf-8'), email=mail, userType=userType)
                # Add the user to the database
                db.session.add(user)
                # Commit the changes made
                db.session.commit()
                login_user(user, True)
                return redirect(url_for("home"))
            else:
                flash("Username already taken!")
        else:
            flash("Passwords aren't identical")

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    return render_template("signup.html")


@app.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash("Username and password must be supplied")
        else:
            if request.method == "POST":
                user = Users.query.filter_by(
                    username=request.form.get("username")).first()
                # Check if the password entered is the
                # same as the user's password
                if bcrypt.check_password_hash(bcrypt.generate_password_hash(password).decode('utf-8'), password):
                    # Use the login_user method to log in the user
                    login_user(user, True)
                    return redirect(url_for("home"))
                else:
                    flash("Password incorrect! Try again.")

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    return render_template("signin.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/home")
@login_required
def home():
    metrics = getDashboardMetrics()
    return render_template("home.html", items=metrics[0], most_common=metrics[1], lowest_amount=metrics[2],
                           rooms=metrics[3], nearest_expiry=metrics[4])


@app.route("/profile")
@login_required
def profil():
    return render_template("profil.html", items=getItems())

@app.route("/inventory")
@login_required
def inventory():
    return render_template("inventory.html", rooms=getRooms(), items=getItems(), currency="€")


@app.route("/edit/<id>", methods=('GET', 'POST'))
@login_required
def editItem(id):
    item = getItem(id)
    if request.method == 'POST':
        item = request.form['item']
        room = request.form['rooms-datalist']
        amount = request.form['amount']
        price = request.form['price']
        weight = request.form['weight']
        color = request.form['color']
        expiry = request.form['expiry']

        conn = sqlite3.connect('instance/inventar.db')
        cursor = conn.cursor()

        # get room id
        cursor.execute(
            "SELECT rooms.id, rooms.name FROM rooms WHERE rooms.name = ?",
            (room, ))
        room_id = cursor.fetchone()[0]

        cursor.execute("UPDATE items SET name = ?, amount = ?, price = ?, weight = ?, color = ?, expiry_date = ?, room_id = ? WHERE id = ?", (item, amount, price, weight, color, expiry, room_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('inventory'))

    return render_template("edit.html", item=item, rooms=getRooms())

@app.route("/new", methods=('GET', 'POST'))
@login_required
def newItem():
    if request.method == 'POST':
        item = request.form['item']
        room = request.form['rooms-datalist']
        amount = request.form['amount']
        price = request.form['price']
        weight = request.form['weight']
        color = request.form['color']
        expiry = request.form['expiry']

        conn = sqlite3.connect('instance/inventar.db')
        cursor = conn.cursor()

        # get room id
        cursor.execute("SELECT rooms.id, rooms.name FROM rooms WHERE rooms.name = ?", (room, ))
        room_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO items (name, amount, price, weight, color, expiry_date, room_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (item, amount, price, weight, color, expiry, room_id))
        conn.commit()
        conn.close()
        return redirect(url_for('inventory'))

    return render_template("new.html", rooms=getRooms())

@app.route("/new_room", methods=('GET', 'POST'))
@login_required
def newRoom():
    if request.method == 'POST':
        room = request.form['room']

        conn = sqlite3.connect('instance/inventar.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO rooms (name) VALUES (?)", (room, ))
        conn.commit()
        conn.close()
        return redirect(url_for('inventory'))

    return render_template("new_room.html")

@app.route('/settings')
@login_required
def settings():
    return render_template("settings.html")

if __name__ == '__main__':
    pass
    app.run(debug=False)
