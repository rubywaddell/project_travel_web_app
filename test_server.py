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

if __name__ == "__main__":
    unittest.main()