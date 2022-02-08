from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import select
from flask_login import login_user, login_required, logout_user, current_user

from website.views import home
from .models import User
from . import db
auth = Blueprint("auth", __name__)

@auth.route('/logout')
@login_required
def logout():
    logout_user() 
    flash("Logged Out Successfully!", category="success")
    return redirect(url_for('views.home'))

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
       # print("here is our check right here ",my_check)
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Log in Succesfull", category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
                #new_user=User()
            else:
                flash("Password Incorrect", category='error')
        else:
            flash("Invalid Email", category='error')

    return render_template("login.html", user=current_user)


@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():

    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print("email",email)
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email is already taken", category="error")
        elif password1 != password2:
            flash("Password does not math", category='error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(email=email).first()
            flash("Thank you for your sign up ", category='success')
            login_user(user, remember=True)
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)