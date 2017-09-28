# -*- encoding: utf-8 -*-
# tests.py

import os
import unittest

from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import User, Group, Role, Tool


basedir = os.path.abspath(os.path.dirname(__file__)) + str('/instance')


class TestBase(TestCase):
    """
    Common testcase.
    """
    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
                 SQLALCHEMY_DATABASE_URI='sqlite:///%s' %
                                         str(os.path.join(basedir,
                                                          'testing.sqlite'))
        )
        return app

    def set_up(self):
        """
        Will be called before every test.
        :return:
        """
        db.create_all()
        test_admin = User(name='test_admin',
                          password='admin2017',
                          is_admin=True)
        test_user = User(name='test_user',
                         password='user2017')
        db.session.add(test_admin)
        db.session.add(test_user)
        db.session.commit()

    def tear_down(self):
        """
        Will be called after every test.
        :return:
        """
        db.session.remove()
        db.drop_all()


class TestModel(TestBase):
    """
    Models testcase.
    """
    def test_user_model(self):
        """
        Test number of records in User table.
        :return:
        """
        self.assertEqual(User.query.count(), 2)

    def test_group_model(self):
        """
        Test number of records in Group table.
        :return:
        """
        group = Group(name='Tester Group', description='The Tester Group')
        db.session.add(group)
        db.session.commit()
        self.assertEqual(Group.query.count(), 1)

    def test_role_model(self):
        """
        Test number of records in Role table.
        :return:
        """
        role = Role(name='Test Role', description='The Test Role')
        db.session.add(role)
        db.session.commit()
        self.assertEqual(Role.query.count(), 1)

    def test_tool_model(self):
        """
        Test number of records in Tool table.
        :return:
        """
        tool = Tool(name='Test Tool', description='The Test Tool')


class TestView(TestBase):
    """
    View testcase.
    """
    def test_home_welcome_view(self):
        """
        Test the welcome page is accessible without signin.
        :return:
        """
        response = self.client.get(url_for('home.welcome_home'))
        self.assertEqual(response.status_code, 200)

    def test_signin_view(self):
        """
        Test the signin page is accessible without signin.
        :return:
        """
        response = self.client.get(url_for('auth.signin'))
        self.assertEqual(response.status_code, 200)

    def test_signout_view(self):
        """
        Test that signout page is inaccessible without signin
        and redirects to signin page then to signout.
        :return:
        """
        target_url = url_for('auth.signout')
        redirect_url = url_for('auth.signin', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_home_user_view(self):
        """
        Test that user home page is inaccessible without signin
        and redirects to signin page then to user page.
        :return:
        """
        target_url = url_for('home.user_home')
        redirect_url = url_for('auth.signin', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_welcome_admin_view(self):
        """
        Test that admin home page is inaccessible without signin
        and redirects to signin page then to admin page.
        :return:
        """
        target_url = url_for('home.admin_home')
        redirect_url = url_for('auth.signin', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_list_groups_view(self):
        """
        Test that groups page is inaccessible without signin
        and redirects to signin page then to groups page.
        :return:
        """
        target_url = url_for('admin.list_groups')
        redirect_url = url_for('auth.signin', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_list_roles_view(self):
        """
        Test that roles page is inaccessible without signin
        and redirects to signin page then to roles page.
        :return:
        """
        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.signin', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_list_users_view(self):
        """
        Test that users page is inaccessible without signin
        and redirects to signin page then to users page.
        :return:
        """
        target_url = url_for('admin.list_users')
        redirect_url = url_for('auth.signin', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_list_tools_view(self):
        """
        Test that tools page is inaccessible withour signin
        and redirects to signin page then to tools page.
        :return:
        """
        target_url = url_for('admin.list_tools')
        redirect_url = url_for('auth.signin', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestError(TestBase):
    """
    Error testcase.
    """
    def test_403_forbidden_error(self):
        """
        Test error 403 forbidden error by creating
        an temporary route.
        :return:
        """
        @self.app.route('/403')
        def forbidden_error():
            abort(403)
        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue('403 Error' in response.data)

    def test_404_page_not_found_error(self):
        """
        Test error 404 page not found error by creating
        an temporary route.
        :return:
        """
        @self.app.route('/404')
        def page_not_found():
            abort(404)
        response = self.client.get('/404')
        self.assertEqual(response.status_code, 404)
        self.assertTrue('404 Error' in response.data)

    def test_500_internal_server_error(self):
        """
        Test error 500 internal server error by creating
        an temporary route.
        :return:
        """
        @self.app.route('/500')
        def internal_server_error():
            abort(500)
        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue('500 Error' in response.data)


if __name__ == '__main__':
    unittest.main()
