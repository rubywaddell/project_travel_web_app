"""Tests to ensure seed_database.py is functioning propery"""

import unittest
import os

from server import app
# import crud
import model
import seed_database

os.system('dropdb travel_project')
os.system('createdb travel_project')


class TestSeedDatabase(unittest.TestCase):
    """Tests for Seed Database file"""

    def test_user_seeded_to_db(self):
        """Test that the users table has successfully been seeded with test data"""

        seed_users = seed_database.seed_users_table()
        test_length = 10
        self.assertEqual(test_length, len(seed_users))
    
    def test_travel_seeded_to_db(self):
        """Test that the travels table has successfully been seeded with test data"""

        seed_travels = seed_database.seed_travels_table()
        test_length = 10
        self.assertEqual(test_length, len(seed_travels))

if __name__ == "__main__":
    unittest.main()