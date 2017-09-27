# -*- coding: utf-8 -*-
# app/home/views.py

from flask import abort, render_template
from flask_login import current_user
from flask_login import login_required as signed_session

from . import home


@home.route('/')
def welcome_home():
    """
    Render the homepage template on the / route
    :return:
    """
    return render_template('home/welcome.html', title='Welcome')


@home.route('/home')
@signed_session
def user_home():
    """
    Render the frontend template on the /home route.
    :return:
    """
    return render_template('home/home.html', title='Home')


@home.route('/admin/home')
@signed_session
def admin_home():
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin.html', title='Admin')
