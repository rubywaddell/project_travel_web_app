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

if __name__ == "__main__":
    unittest.main()