# -*- coding: utf-8 -*-
# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, lm


class User(UserMixin, db.Model):
    """
    Create an User table.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    name = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent password from been accessed.
        :return:
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to hashed password.
        :param password:
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password match actual password.
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: %s>' % self.username


# Set up user_loader                                                                    
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Group(db.Model):
    """
    Create a Group table.
    """
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='group', lazy='dynamic')

    def __repr__(self):
        return '<Group: %s>' % self.name


class Role(db.Model):
    """
    Create a Role table
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: %s>' % self.name


class Tool(db.Model):
    """
    Create a Tool table.
    """
    __tablename__ = 'tools'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    target = db.Column(db.String(200))

    def __repr__(self):
        return '<Tool: %s>' % self.name
