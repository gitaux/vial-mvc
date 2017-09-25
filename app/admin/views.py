# -*- coding: utf-8 -*-
# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import GroupForm, ToolForm
from .. import db
from ..models import Group, Tool


def check_admin():
    """
    Prevent non-admins from accessing the page.
    :return: 
    """
    if not current_user.is_admin:
        abort(403)


@admin.route('/groups', methods=['GET', 'POST'])
@login_required
def list_groups():
    """
    List all groups.
    :return:
    """
    check_admin()
    groups = Group.query.all()
    return render_template('admin/groups/list_groups.html',
                           title='Groups',
                           groups=groups)


@admin.route('/groups/add', methods=['GET', 'POST'])
@login_required
def add_group():
    """
    Add a group to the database.
    :return:
    """
    check_admin()
    add_group = True
    form = GroupForm()
    if form.validate_on_submit():
        group = Group(name=form.name.data,
                      description=form.description.data)
        db.session.add(group)
        db.session.commit()
        flash('You have successfully added a new group.')
        return redirect(url_for('admin.list_groups'))
    return render_template('admin/groups/add_group.html',
                           title='Add Group',
                           add_group=add_group,
                           action='Add',
                           form=form)


@admin.route('/groups/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_group(id):
    """
    Edit a group.
    :param id:
    :return:
    """
    check_admin()
    group = Group.query.get_or_404(id)
    form = GroupForm(obj=group)
    if form.validate_on_submit():
        group.name = form.name.data
        group.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the group.')
        return redirect(url_for('admin.list_groups'))
    form.description.data = group.description
    form.name.data = group.name
    return render_template('admin/groups/list_groups.html',
                           title='Edit Group',
                           action='Edit',
                           group=group,
                           form=form)


@admin.route('/groups/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_group(id):
    """
    Deletes a group from the database.
    :param id:
    :return:
    """
    check_admin()
    group = Group.query.get_or_404(id)
    form = GroupForm(obj=group)
    if form.validate_on_submit():
        db.session.delete(group)
        db.session.commit()
        flash('You have successfully deleted the group.')
        return redirect(url_for('admin.list_groups'))
    return render_template('admin/groups/delete_group.html',
                          title="Delete Group",
                          action='Delete',
                          group=group,
                          form=form)


@admin.route('/tools', methods=['GET', 'POST'])
@login_required
def list_tools():
    """
    List all tools.
    :return:
    """
    check_admin()
    tools = Tool.query.all()
    return render_template('admin/tools/list_tools.html',
                           title='Tools',
                           tools=tools)


@admin.route('/tools/add', methods=['GET', 'POST'])
@login_required
def add_tool():
    """
    Add a tool to the database.
    :return:
    """
    check_admin()
    form = ToolForm()
    if form.validate_on_submit():
        tool = Tool(name=form.name.data,
                    description=form.description.data,
                    target=form.target.data)
        db.session.add(tool)
        db.session.commit()
        flash('You have successfully added a new tool.')
        return redirect(url_for('admin.list_tools'))
    return render_template('admin/tools/add_tool.html',
                           title='Add Tool',
                           action='Add',
                           form=form)
