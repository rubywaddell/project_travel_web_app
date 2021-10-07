"""Tests for server.py file"""
import unittest
import os

import server
import crud
import model

os.system('dropdb travel_project')
os.system('createdb travel_project')

class TestHomePageRoutes(unittest.TestCase):
    """Tests for HomePage view functions"""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config["TESTING"] = True

    def test_homepage_route(self):
        """Test that the homepage loads when / route is accessed"""

        result = self.client.get("/")
        self.assertIn(b"Welcome!", result.data)
    
    def test_homepage_navigation(self):
        """Test that the homepage links to other pages in the site"""

        result = self.client.get("/")
        self.assertIn(b"<ul>Navigation:</ul>", result.data)

class TestLoginPage(unittest.TestCase):
    """Tests for Log In page view functions"""

    #TESTS STILL NEED TO WRITE:
        #- Test that only existing users can log in
        #- Test that non-existant users get redirected to create account page

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config["TESTING"] = True

    def test_login_route(self):
        """Test that the /login route opens the Log In page"""

        result = self.client.get("/login")
        self.assertIn(b"""<input type="password" name="password">""", result.data)   

    def test_login_post_method(self):
        """Test that the /login route uses a POST method to keep passwords safer"""

        result = self.client.get("/login")
        self.assertIn(b'method="POST"', result.data) 
    
    def test_login_form_action(self):
        """Test that the login form routes to the user profile page once they are logged in"""

        result = self.client.get("/login")
        self.assertIn(b'action="/profile/<username>"', result.data)

class TestViewTipsPage(unittest.TestCase):
    """Test for the view_travel_tips page"""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config["TESTING"] = True

    def test_view_tip_route(self):
        """Test that the view_travel_tips route opens properly"""

        result = self.client.get("/view_travel_tips")
        self.assertIn(b"<h2>All Travel Tips:</h2>", result.data) 

    def test_view_tip_table(self):
        """Test that the travel tips are displaying in an HTML table"""
        result = self.client.get("/view_travel_tips")
        self.assertIn(b"<table>", result.data)


if __name__ == "__main__":
    unittest.main()