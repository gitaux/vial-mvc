# -*- coding: utf-8 -*-
# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an User to the through the registration form
    :return:
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.name.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('You have successfully registered! You may now login.')
        except:
            db.session.fallback()
            flash('Failed to register new user.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',
                           title='Register',
                           form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route.
    Log an user in through the login form.
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        else:
            flash('Invalid email or password.')
    return render_template('auth/login.html',
                           title='Login',
                           form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route.
    Log an user out through the logout form.
    :return:
    """
    logout_user()
    flash('You have successfully been logged out.')
    return redirect(url_for('auth.login'))
