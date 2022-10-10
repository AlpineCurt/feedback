from crypt import methods
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import NewUserForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback" # need a database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = 'ilikecoffeeiliketea'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

toolbar=DebugToolbarExtension(app)

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    GET will display form to register new user
    POST will create the new user
    """
    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(
            username = username,
            password = password,
            email = email,
            first_name = first_name,
            last_name = last_name
        )
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken.  Please pick another")
            return render_template("register.html", form=form)
        session["user_id"] = new_user.username
        flash("Welcome!  Account creation successful", "success")
        return redirect("/secret")

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    GET will display login page.
    POST will log a user in
    """
    form = LoginForm()

    return render_template("login.html", form=form)

@app.route("/secret")
def secret_route():
    return render_template("secret.html")