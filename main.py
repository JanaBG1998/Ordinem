from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import *
from flask_bcrypt import Bcrypt
import sqlite3
from flask_sqlalchemy import SQLAlchemy





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


# Initialize app with extension
db.init_app(app)
# Create database within app context

with app.app_context():
	db.create_all()

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

        if not username or not password or not repassword:
            flash('Username and password must be supplied!')
        else:
            pass
        if password == repassword:
            if not Users.query.filter_by(
        username=request.form.get("username")).first():
                user = Users(username=username,
                             password=bcrypt.generate_password_hash(password).decode('utf-8'))
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
def logout():
    logout_user()
    return redirect("/")

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

if __name__ == '__main__':
    pass
    app.run(debug=False)





