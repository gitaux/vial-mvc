# -*- coding: utf-8 -*-
# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField  # , BooleanField
from wtforms.validators import DataRequired, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Group, Role


class UserForm(FlaskForm):
    """
    From admin to assign groups and roles to users.
    """
    email = StringField('Email', validators=[DataRequired(),
                                             Email()])
    name = StringField('Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    group = QuerySelectField(query_factory=lambda: Group.query.all(),
                             get_label='name')
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label='name')
    submit = SubmitField('Submit')


class GroupForm(FlaskForm):
    """
    Form admin to add or edit a group.
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    """
    Form admin to add or edit a role.
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ToolForm(FlaskForm):
    """
    Form admin to add or edit a tool.
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
