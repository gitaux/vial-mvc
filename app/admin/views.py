# -*- coding: utf-8 -*-
# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required as signed_session

from . import admin
from forms import GroupForm, RoleForm, ToolForm, UserForm
from .. import db
from ..models import Group, Role, Tool, User


def check_admin():
    """
    Prevent non-admins from accessing the page.
    :return:
    """
    if not current_user.is_valid and not current_user.is_admin:
        abort(403)


@admin.route('/groups', methods=['GET', 'POST'])
@signed_session
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
@signed_session
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
            db.session.add(group)  # type: Group
            db.session.commit()
            flash('You have successfully added a new group: "%s".' %
                  str(group.name))
        except AttributeError:
            db.session.rollback()
            flash('Failed to add the group: "%s".' %
                  str(group.name))
        return redirect(url_for('admin.list_groups'))
    return render_template('admin/groups/add_group.html',
                           title='Add Group',
                           action='Add',
                           form=form)  # type: GroupForm


@admin.route('/groups/edit/group-<int:id>', methods=['GET', 'POST'])
@signed_session
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
            flash('You have successfully edited the group: "%s".' %
                  str(group.name))
        except AttributeError:
            db.session.rollback()
            flash('Failed to edit the group: "%s".' %
                  str(group.name))
        return redirect(url_for('admin.list_groups'))
    form.description.data = group.description
    form.name.data = group.name
    return render_template('admin/groups/edit_group.html',
                           title='Edit Group',
                           action='Edit',
                           group=group,
                           form=form)  # type: GroupForm


@admin.route('/groups/delete/group-<int:id>', methods=['GET', 'POST'])
@signed_session
def delete_group(id):
    """
    Deletes a group from the database.
    :param id:
    :return:
    """
    check_admin()
    group = Group.query.get_or_404(id)
    try:
        db.session.delete(group)
        db.session.commit()
        flash('You have successfully deleted the group: "%s".' %
              str(group.name))
    except AttributeError:
        db.session.rollback()
        flash('failed to delete the group: "%s".' %
              str(group.name))
    return redirect(url_for('admin.list_groups'))


@admin.route('/roles')
@signed_session
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
@signed_session
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
            flash('Successfully added a new role: "%s".' %
                  str(role.name))
        except AttributeError:
            db.session.rollback()
            flash('Error: role name already exists: "%s".' %
                  str(role.name))
        return redirect(url_for('admin.list_roles'))
    return render_template('admin/roles/add_role.html',
                           title='Add Role',
                           form=form)  # type: RoleForm


@admin.route('/roles/edit/role-<int:id>', methods=['GET', 'POST'])
@signed_session
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
            flash('Successfully edited the role: "%s".' %
                  str(role.name))
        except AttributeError:
            db.session.rollback()
            flash('failed to edit the role: "%s".' %
                  str(role.name))
        return redirect(url_for('admin.list_roles'))
    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/edit_role.html',
                           title='Edit Role',
                           form=form)  # type: RoleForm


@admin.route('/roles/delete/role-<int:id>', methods=['GET', 'POST'])
@signed_session
def delete_role(id):
    """
    Delete a role from the database.
    :param id:
    :return:
    """
    check_admin()
    role = Role.query.get_or_404(id)
    try:
        db.session.delete(role)
        db.session.commit()
        flash('Successfully deleted the role: "%s".' %
              str(role.name))
    except AttributeError:
        db.session.rollback()
        flash('Failed to delete the role: "%s".' %
              str(role.name))
    return redirect(url_for('admin.list_roles'))


@admin.route('/tools', methods=['GET', 'POST'])
@signed_session
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
@signed_session
def add_tool():
    """
    Add a tool to the database.
    :return:
    """
    check_admin()
    form = ToolForm()
    if form.validate_on_submit():
        tool = Tool(name=form.name.data,
                    description=form.description.data)
        try:
            db.session.add(tool)
            db.session.commit()
            flash('Successfully added a new tool: "%s".' %
                  str(tool.name))
        except AttributeError:
            db.session.rollback()
            flash('Failed to add the tool: "%s".' %
                  str(tool.name))
        return redirect(url_for('admin.list_tools'))
    return render_template('admin/tools/add_tool.html',
                           title='Add Tool',
                           action='Add',
                           form=form)  # type: ToolForm


@admin.route('/tools/edit/tool-<int:id>', methods=['GET', 'POST'])
@signed_session
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
        try:
            db.session.add(tool)
            db.session.commit()
            flash('Successfully edited the tool: "%s".' %
                  str(tool.name))
        except AttributeError:
            db.session.rollback()
            flash('Failed to edit the tool: "%s".' %
                  str(tool.name))
        return redirect(url_for('admin.list_tools'))
    form.name.data = tool.name
    form.description.data = tool.description
    return render_template('admin/tools/edit_tool.html',
                           title='Edit Tool',
                           tool=tool,
                           form=form)  # type: ToolForm


@admin.route('/tools/delete/tool-<int:id>', methods=['GET', 'POST'])
@signed_session
def delete_tool(id):
    """
    Delete an tool from the database.
    :param id:
    :return:
    """
    check_admin()
    tool = Tool.query.get_or_404(id)
    try:
        db.session.delete(tool)
        db.session.commit()
        flash('Successfully deleted the tool: "%s".' %
              str(tool.name))
    except AttributeError:
        db.session.rollback()
        flash('Failed to delete to tool: "%s".' %
              str(tool.name))
    return redirect(url_for('admin.list_tools'))


@admin.route('/users')
@signed_session
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


@admin.route('/users/edit/user-<int:id>', methods=['GET', 'POST'])
@signed_session
def edit_user(id):
    """
    Edit users.
    :param id:
    :return:
    """
    check_admin()
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.name = form.name.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        try:
            db.session.add(user)
            db.session.commit()
            flash('Successfully edited the user: "%s".' %
                  str(user.name))
        except AttributeError:
            db.session.rollback()
            flash('Failed to edit the user: "%s".' %
                  str(user.name))
        return redirect(url_for('admin.list_users'))
    form.email.data = user.email
    form.name.data = user.name
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    return render_template('admin/users/edit_user.html',
                           title='Edit User',
                           user=user,
                           form=form)  # type: UserForm


@admin.route('/users/assign/user-<int:id>', methods=['GET', 'POST'])
@signed_session
def assign_user(id):
    """
    Assign a group and a role to an user.
    :param id:
    :return:
    """
    check_admin()
    user = User.query.get_or_404(id)
    if user.is_admin:
        abort(403)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.group = form.group.data  # type: UserForm
        user.role = form.role.data
        try:
            db.session.add(user)
            db.session.commit()
            flash('Successfully assigned "%s" to "%s" as "%s".' %
                  (str(user.name),
                   str(user.group),
                   str(user.role)))
        except AttributeError:
            db.session.rollback()
            flash('Failed to assign group and role to: "%s".' %
                  str(user.name))
        return redirect(url_for('admin.list_users'))
    form.group.data = user.group
    form.role.data = user.role
    return render_template('admin/users/assign_user.html',
                           title='Assign User',
                           user=user,
                           form=form)  # type: UserForm


@admin.route('/users/delete/user-<int:id>', methods=['GET', 'POST'])
@signed_session
def delete_user(id):
    """
    Delete an user from the database.
    :param id:
    :return:
    """
    check_admin()
    user = User.query.get_or_404(id)
    if user.is_admin:
        abort(403)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted the user: "%s".' %
              str(user.name))
    except AttributeError:
        db.session.rollback()
        flash('Failed to delete the user: "%s".' %
              str(user.name))
    return redirect(url_for('admin.list_users'))
