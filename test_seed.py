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

    def test_user_w_travel_id_seeded_to_db(self):
        """Test that the users table has successfully been seeded with test users that are related to travels table"""

        seed_users = seed_database.users_in_db
        test_travel_id = 1
        test_user = seed_users[0]
        self.assertEqual(test_travel_id, test_user.travel_id)
    
    def test_travel_seeded_to_db(self):
        """Test that the travels table has successfully been seeded with test data"""

        seed_travels = seed_database.seed_travels_table()
        test_length = 10
        self.assertEqual(test_length, len(seed_travels))

    def test_state_seeded_to_db(self):
        """Test that the states table has successfully been seeded with example data"""

        seed_states = seed_database.seed_states_table()
        test_length = 50
        self.assertEqual(test_length, len(seed_states))

    def test_city_seeded_to_db(self):
        """Test that the cities table has successfully been seeded with exmaple data"""

        seed_cities = seed_database.seed_cities_table()
        test_length = 10
        self.assertEqual(test_length, len(seed_cities))

    def test_tip_seeded_to_db(self):
        """Testt that the tips table has successfully been seeded with example data"""

        seed_tips = seed_database.seed_tips_table()
        test_length = 10
        self.assertEqual(test_length, len(seed_tips))

    def test_tag_seeded_to_db(self):
        """Test that the tags table has successfully been seeded with data"""

        seed_tags = seed_database.seed_tags_table()
        test_length = 10
        self.assertEqual(test_length, len(seed_tags))


if __name__ == "__main__":
    unittest.main()