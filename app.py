from crypt import methods
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import NewUserForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = 'ilikecoffeeiliketea'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

toolbar=DebugToolbarExtension(app)

@app.route("/")
def home_page():
    if "user_id" in session:
        user = User.query.filter_by(username=session["user_id"]).first()
        return render_template("index.html", user=user)
    else:
        return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    GET will display form to register new user
    POST will create the new user
    """
    form = NewUserForm()
    if form.validate_on_submit():       
        new_user = User.register(
            username = form.username.data,
            password = form.password.data,
            email = form.email.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data
        )
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken.  Please pick another")
            return render_template("register.html", form=form)
        session["user_id"] = new_user.username
        flash("Welcome!  Account creation successful", "success")
        return redirect("f/users/{user.username}")

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    GET will display login page.
    POST will log a user in
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            flash(f"Welcome back, {user.username}!", "primary")
            session["user_id"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username or password.']

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Logs out a user"""
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect("/")

@app.route("/users/<username>")
def user_info(username):
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    user = User.query.filter_by(username=username).first()
    return render_template('user_info.html', user=user)

@app.route("/users/<string:username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    user = User.query.filter_by(username=username).first()
    if session["user_id"] != username:
        flash("You can post for your account only.", "danger")
        return redirect("/")
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            title=form.title.data,
            content=form.content.data,
            username=username
            )
        db.session.add(feedback)
        db.session.commit()
        flash('Feedback added!', 'success')
        return redirect(f"/users/{username}")

    return render_template("feedback.html", form=form, user=user)


@app.route("/secret")
def secret_route():
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        user = User.query.filter_by(username=session["user_id"]).first()
        return render_template("secret.html", user=user)