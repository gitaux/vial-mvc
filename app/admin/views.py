# -*- coding: utf-8 -*-
# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import GroupForm, RoleForm, ToolForm, UserAssignForm
from .. import db
from ..models import Group, Role, Tool, User


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
    form = GroupForm()
    if form.validate_on_submit():
        group = Group(name=form.name.data,
                      description=form.description.data)
        try:
            db.session.add(group)
            db.session.commit()
            flash('You have successfully added a new group.')
        except:
            db.session.rollback()
            flash('Failed to add the group.')
        return redirect(url_for('admin.list_groups'))
    return render_template('admin/groups/add_group.html',
                           title='Add Group',
                           action='Add',
                           form=form)


@admin.route('/groups/edit/group-<int:id>', methods=['GET', 'POST'])
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
        try:
            db.session.add(group)
            db.session.commit()
            flash('You have successfully edited the group.')
        except:
            db.session.rollback()
            flash('Failed to edit the group.')
        return redirect(url_for('admin.list_groups'))
    form.description.data = group.description
    form.name.data = group.name
    return render_template('admin/groups/edit_group.html',
                           title='Edit Group',
                           action='Edit',
                           group=group,
                           form=form)


@admin.route('/groups/delete/group-<int:id>', methods=['GET', 'POST'])
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
        try:
            db.session.delete(group)
            db.session.commit()
            flash('You have successfully deleted the group.')
        except:
            db.session.rollback()
            flash('failed to delete the group.')
        return redirect(url_for('admin.list_groups'))
    return render_template('admin/groups/delete_group.html',
                           title="Delete Group",
                           action='Delete',
                           group=group,
                           form=form)


@admin.route('/roles')
@login_required
def list_roles():
    """
    List all roles.
    :return:
    """
    check_admin()
    roles = Role.query.all()
    return render_template('admin/roles/list_roles.html',
                           title='Roles',
                           roles=roles)


@admin.route('roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database.
    :return:
    """
    check_admin()
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)
        try:
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            db.session.rollback()
            flash('Error: role name already exists.')
        return redirect(url_for('admin.list_roles'))
    return render_template('admin/roles/add_role.html',
                           title='Add Role',
                           form=form)


@admin.route('/roles/edit/role-<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role.
    :param id:
    :return:
    """
    check_admin()
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        try:
            db.session.add(role)
            db.session.commit()
            flash('You have successfully edited the role.')
        except:
            db.session.rollback()
            flash('failed to edit the role.')
        return redirect(url_for('admin.list_roles'))
    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/edit_role.html',
                           title='Edit Role',
                           form=form)


@admin.route('/roles/delete/role-<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database.
    :param id:
    :return:
    """
    check_admin()
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        try:
            db.session.delete(role)
            db.session.commit()
            flash('You have successfully deleted the role.')
        except:
            db.session.rollback()
            flash('Failed to delete the role.')
        return redirect(url_for('admin.list_roles'))
    return render_template('admin/roles/delete_role.html',
                           title='Delete Role',
                           role=role,
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
        try:
            db.session.add(tool)
            db.session.commit()
            flash('You have successfully added a new tool.')
        except:
            db.session.rollback()
            flash('Failed to add the tool.')
        return redirect(url_for('admin.list_tools'))
    return render_template('admin/tools/add_tool.html',
                           title='Add Tool',
                           action='Add',
                           form=form)


@admin.route('/tools/edit/tool-<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tool(id):
    """
    Edit a tool.
    :param id:
    :return:
    """
    check_admin()
    tool = Tool.query.get_or_404(id)
    form = ToolForm(obj=tool)
    if form.validate_on_submit():
        tool.name = form.name.data
        tool.description = form.description.data
        tool.target = form.target.data
        try:
            db.session.add(tool)
            db.session.commit()
            flash('Successfully edited the tool.')
        except:
            db.session.rollback()
            flash('Failed to edit the tool')
        return redirect(url_for('admin.list_tools'))
    form.name.data = tool.name
    form.description.data = tool.description
    form.target.data = tool.target
    return render_template('admin/tools/edit_tool.html',
                           title='Edit Tool',
                           tool=tool,
                           form=form)


@admin.route('/tools/delete/tool-<int:id>', methods=['GET', 'POST'])
@login_required
def delete_tool(id):
    """
    Delete a tool from the database.
    :param id:
    :return:
    """
    check_admin()
    tool = Tool.query.get_or_404(id)
    form = ToolForm(obj=tool)
    if form.validate_on_submit():
        tool.name = form.name.data
        tool.description = form.description.data
        tool.target = form.target.data
        try:
            db.session.delete(tool)
            db.session.commit()
            flash('Successfully deleted the tool.')
        except:
            db.session.rollback()
            flash('Failed to delete to tool.')
        return redirect(url_for('admin.list_tools'))
    form.name.data = tool.name
    form.description.data = tool.description
    form.target.data = tool.target
    return render_template('admin/tools/delete_tool.html',
                           title='Delete Tool',
                           tool=tool,
                           form=form)


@admin.route('/users')
@login_required
def list_users():
    """
    List all users.
    :return:
    """
    check_admin()
    users = User.query.all()
    return render_template('admin/users/list_users.html',
                           title='Users',
                           users=users)
