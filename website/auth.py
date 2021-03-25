from flask import Blueprint, render_template, redirect, request, flash, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET","POST"])
def login():
   if request.method == "POST":
      email = request.form.get("email")
      password = request.form.get("password")

      user = User.query.filter_by(email = email).first()
      if user:
         if check_password_hash(user.password, password):
            flash("Logged in Successfully!", category = "success")
            login_user(user, remember=True)
            return redirect(url_for("views.home"))
         else:
            flash("Incorrect Password!", category = "error")
      else:
         flash("Email does not exist !", category="error")

   return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for("auth.login"))

@auth.route('/signup', methods=["GET","POST"])
def signup():
   if request.method == "POST":
      email = request.form.get("email")
      name = request.form.get("Full Name")
      password1 = request.form.get("password1")
      password2 = request.form.get("password2")

      user = User.query.filter_by(email = email).first()

      if user:
         flash("User already exists!", category="error")
      elif len(email) < 12:
         flash("Email is Incorrect!", category="error")
      elif len(name) < 5:
         flash("Please enter your full name!", category="error")
      elif len(password1) < 6:
         flash("Password too short!", category="error")
      elif password1 != password2:
         flash("Passwords don't match", category="error")
      else:
         new_user = User(email=email,password=generate_password_hash(password1, method="sha256"), name=name)
         db.session.add(new_user)
         db.session.commit()
         # login_user(user, remember=True)
         flash("Congratulations! Account created. ", category="success")
         return redirect(url_for("auth.login"))

   return render_template("sign_up.html",user=current_user)
