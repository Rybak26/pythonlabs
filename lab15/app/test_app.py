# app/test_app.py

import unittest
from os.path import abspath, dirname
import sys

from flask_testing import TestCase as FlaskTestCase

sys.path.append(dirname(dirname(abspath(__file__))))
from app.create_app import create_app, db
from app.models import User, Todo


class TestApp(FlaskTestCase):

    def create_app(self):
        """Create and configure the Flask app for testing."""
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        """Set up the test environment."""
        db.create_all()
        self.test_objects = []

    def tearDown(self):
        """Tear down the test environment and clean up test objects."""
        for obj in self.test_objects:
            db.session.delete(obj)
        db.session.commit()

    def test_homepage(self):
        """Test if the homepage is accessible and contains 'Register'."""
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)
        print(f"Check homepage are successful! {response}")

    def test_register_and_login(self):
        """Test user registration, login, logout, login after logout, and profile changes."""
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'submit': 'Register'
        })
        self.assertIn(response.status_code, [200, 302])
        print(f"Register are successful! {response}")

        response = self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'submit': 'Login'
        })
        self.assertEqual(response.status_code, 302)
        print(f"Login are successful! {response}")

        user = User.query.filter_by(username='testuser').first()
        self.test_objects.append(user)

        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        print(f"Logout are successful! {response}")

        response = self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'submit': 'Login'
        })
        self.assertEqual(response.status_code, 302)
        print(f"Login after logout are successful! {response}")

        user = User.query.filter_by(username='testuser').first()
        self.test_objects.append(user)

        response = self.client.post('/account', data={
            'username': 'newusername',
            'email': 'newemail@example.com',
            'submit': 'Update'
        })
        self.assertEqual(response.status_code, 302)
        print(f"Profile change are successful! {response}")

        updated_user = User.query.filter_by(username='newusername').first()
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.email, 'newemail@example.com')

    def test_todo_crud_operations(self):
        """Test Todo CRUD operations."""
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'submit': 'Register'
        })
        self.assertIn(response.status_code, [200, 302])
        print(f"Register are successful! {response}")

        response = self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'submit': 'Login'
        })
        self.assertEqual(response.status_code, 302)
        print(f"Login are successful! {response}")

        response = self.client.post('/addtodo', data={
            'title': 'Test Todo',
            'description': 'This is a test todo.',
            'completed': 'Submit'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print(f"Add todo are successful! {response}")

        created_todo = Todo.query.filter_by(title='Test Todo').first()
        self.assertIsNotNone(created_todo)
        self.assertEqual(created_todo.description, 'This is a test todo.')

        response = self.client.post(f'/edittodo/{created_todo.id}', data={
            'title': 'Updated Todo',
            'description': 'This is an updated todo.',
            'completed': 'Submit'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        updated_todo = Todo.query.get(created_todo.id)
        self.assertIsNotNone(updated_todo)
        self.assertEqual(updated_todo.title, 'Updated Todo')
        self.assertEqual(updated_todo.description, 'This is an updated todo.')
        print(f"Edit todo are successful! {response}")

        response = self.client.get(f'/edittodo/{created_todo.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Todo', response.data)
        print(f"Read todo are successful! {response}")

        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        print(f"Logout are successful! {response}")

        self.test_objects.append(created_todo)


if __name__ == '__main__':
    unittest.main()
