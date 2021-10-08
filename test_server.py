"""Tests for server.py file"""
import unittest
import os

import server
import seed_mock_data
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
        """Test that the login form routes to the login route
            - will later test to make sure user is in database, then redirect"""

        result = self.client.get("/login")
        self.assertIn(b'action="/login"', result.data)
    
    def test_log_in_existing_user(self):
        """Tests that the login only accepts an existing user profile"""
        users = seed_mock_data.seed_user_w_no_travel()
        user = users[0]
        test_username = bytes(user.username, "utf-8")

        result = self.client.post(f"/profile/{test_username}")

        self.assertIn(test_username, result.data)

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


class TestProfilePage(unittest.TestCase):
    """Test for the user's profile page"""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config["TESTING"] = True
    
    def test_profile_page_route(self):
        """Test that the profile route opens properly"""
        users = seed_mock_data.users_no_travel_in_db
        user = users[0]
        test_username = bytes(user.username, "utf-8")
        result = self.client.post(f"/profile/{test_username}")
        self.assertIn(b"<h2>Your Trips:</h2>", result.data)

class TestCreateAccountPage(unittest.TestCase):
    """Tests for the creat-account page"""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config["TESTING"] = True

    def test_create_account_route(self):
        """Test that the create account route opens properly"""
        result = self.client.get("/create_account")
        self.assertIn(b"Your Travel Information:", result.data)
    
    def test_add_new_user_to_db(self):
        """Test that the new user gets successfully added to the database"""

        result = self.client.post("/create_account")
        

if __name__ == "__main__":
    unittest.main()