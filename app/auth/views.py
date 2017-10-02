# -*- coding: utf-8 -*-
# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required as signed_session
from flask_login import login_user as signin_user
from flask_login import logout_user as signout_user

from . import auth
from forms import SignInForm, SignUpForm
from .. import db
from ..models import User


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handle requests to the /signup route
    Add an User to the through the registration form
    :return:
    """
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.name.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('You have successfully signed up! You may now sign in.')
        except AttributeError:
            db.session.fallback()
            flash('Failed to sign up new user.')
        return redirect(url_for('auth.signin'))
    return render_template('auth/signup.html',
                           title='Sign Up',
                           form=form)


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    """
    Handle requests to the /signin route.
    :return:
    """
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            signin_user(user)
            if user.is_admin:
                return redirect(url_for('home.admin'))
            else:
                return redirect(url_for('home.start'))
        else:
            flash('Invalid email or password.')
    return render_template('auth/signin.html',
                           title='Sign In',
                           form=form)


@auth.route('/signout')
@signed_session
def signout():
    """
    Handle requests to the /signout route.
    :return:
    """
    signout_user()
    flash('You successfully signed out.')
    return redirect(url_for('home.welcome'))
