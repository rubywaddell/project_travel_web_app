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

    def test_home_page_route(self):
        """Test that the home_page loads when / route is accessed"""

        result = self.client.get("/")
        self.assertIn(b"Welcome", result.data)

if __name__ == "__main__":
    unittest.main()