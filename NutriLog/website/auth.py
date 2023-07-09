from flask import Blueprint, request, render_template, redirect, flash, url_for
from .helpers import is_valid_email
from .helpers import is_valid_email
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db, User
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash('You must enter an email', category='error')
        password = request.form.get('password')
        if not password:
            flash('You must enter a password', category='error')

        user = User.query.filter_by(email=email).first()
        if user:
                if check_password_hash(user.password, password):
                    flash('Logged in', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for("pages.diary"))
                else:
                    flash('Incorrect password.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')

@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    
    email = request.form.get('email')
    if not email:
        flash('Enter email', category='error')
        return redirect('/register')
    elif not is_valid_email(email):
        flash('Enter a valid email', category='error')
        return redirect('/register')
    elif User.query.filter_by(email=email).first():
        flash('You already have an account', category='error')
        return redirect('/register')
    else:
        password = request.form.get('password')
        if not password:
            flash('Enter a password', category='error')
            return redirect('/register')
        elif len(password) < 5:
            flash('Password must be a minimum 5 characters long', category='error')
            return redirect('/register')
        else:
            confirmPassword = request.form.get('confirmPassword')
            if not confirmPassword:
                flash('Enter a password', category='error')
                return redirect('/register')
            elif confirmPassword != password:
                flash('Passwords do not match', category='error')
                return redirect('/register')
            
    new_user = User(email=email, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    flash('Account Created', category='success')
    return redirect(url_for('pages.diary'))
    