from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash 

auth = Blueprint('auth',__name__) #defining the Blueprint and naming it as auth

#creating auth routes for Login, Logout and Register

@auth.route('/login',methods = ['GET', 'POST'])
def login():
    #data = request.form
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email == "":
            flash("Email is empty. Please enter Email ID",category='error')
        elif password == "":
            flash("Password is empty. Please enter a Password.", category='error')
        else: 
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password,password):
                    flash('Successfully Logged in!', category='success')
                    login_user(user,remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, Please Try Again!',category='error')
            else:
                flash('Email Id Not found!', category='error')

    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required

def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/Register',methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if email == "":
            flash("Email is empty. Please enter Email ID",category='error')
        elif firstName == "":
            flash("First Name is Empty. Please Enter the First Name",category='error')        
        elif lastName == "":
            flash("Last Name is Empty. Please Enter the Last Name",category='error')
        elif password1 == "":
            flash("Password is empty. Please enter a Password.", category='error')
        elif password2 == "":
            flash("Please confirm the Password.", category='error')
        
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists',category='error')

            if len(email) < 4 :
                flash ('Email must be greater than 4 characters.', category = 'error')
            elif '@' not in email :
                flash ("Please enter a valid email id", category= 'error')
            elif len(firstName) < 2:
                flash ('First Name must be greater than 1 character.', category = 'error')
            elif len(lastName) <2:
                flash ('Last Name must be greater than 1 characters.', category = 'error')
            elif (len(password1) != len(password2)) & (password1 != password2):
                flash ("Passwords don't match.", category = 'error')
            else:
                #adding the user to the database
                if db.session.query(User).filter_by(email=email).count() < 1:
                    new_user = User(email=email, firstName = firstName, lastName = lastName, password=generate_password_hash(password1,method='sha256'))
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user,remember=True)
                    flash ('Account created Successfully!', category = 'success') 
                    return redirect(url_for('views.home'))

        

    return render_template("register.html",user=current_user)
