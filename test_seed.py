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
    
    def test_user_travel_query(self):
        """Test query between user and travel returns the correct attributes"""

        test_user = seed_database.users_in_db[0]
        test_travel = seed_database.travels_in_db[0]

        self.assertEqual(test_travel.travel_id, test_user.travel_id)
        self.assertEqual(test_travel.arrival_date, test_user.travel.arrival_date)

    def test_travel_seeded_to_db(self):
        """Test that the travels table has successfully been seeded with test data"""

        seed_travels = seed_database.seed_travels_table()
        test_length = 10
        self.assertEqual(test_length, len(seed_travels))

    def test_travel_w_state_id_seeded_to_db(self):
        """Test that the travels table has successfully been seeded with test travels that are related to the states tabel"""

        seed_travels = seed_database.travels_in_db
        test_state_id = 1
        test_travel= seed_travels[0]
        self.assertEqual(test_state_id, test_travel.state_id)   

    def test_user_travel_state_query(self):
        """Test that users can be queried through travel table relations"""

        test_travel = seed_database.travels_in_db[0]
        test_state = test_travel.state
        test_user = test_travel.user

        self.assertFalse(test_state == None)
        self.assertFalse(test_user == None)     

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

    def test_tip_w_user_id_seeded_to_db(self):
        """Test that tip objects with relationships to users are successfully seed to database"""

        seed_tips = seed_database.seed_tips_table()
        print("\n*"*5)
        print("Seed_tips list=", seed_tips)
        print("\n*"*5)
        test_user_id = 1
        test_tip = seed_tips[0]

        self.assertEqual(test_user_id, test_tip.user_id)

    def test_tag_seeded_to_db(self):
        """Test that the tags table has successfully been seeded with data"""

        seed_tags = seed_database.seed_tags_table()
        test_length = 10
        self.assertEqual(test_length, len(seed_tags))

    def test_tip_tag_seeded_to_db(self):
        """Test that the tip_tags table has successfully been seeded with data"""

        seed_tip_tags = seed_database.seed_tip_tags_table()
        test_length = 10
        self.assertEqual(test_length, len(seed_tip_tags))

    def test_tip_tag_w_tip_id_seeded_to_db(self):
        """Test that the travels table has successfully been seeded with test travels that are related to the states tabel"""

        seed_tip_tags = seed_database.tip_tags_in_db
        test_tip_id = 1
        test_tip_tag= seed_tip_tags[0]
        self.assertEqual(test_tip_id, test_tip_tag.tip_id)
    
    def test_tip_tag_w_tag_id_seeded_to_db(self):
        """Test that the travels table has successfully been seeded with test travels that are related to the states tabel"""

        seed_tip_tags = seed_database.tip_tags_in_db
        test_tag_id = 1
        test_tip_tag= seed_tip_tags[0]
        self.assertEqual(test_tag_id, test_tip_tag.tag_id)

    def test_tip_tag_to_tag_query(self):
        """Test that query functionality between tip_tag and tag objects is working properly"""

        test_tag = seed_database.tags_in_db[0]
        test_tip_tag = seed_database.tip_tags_in_db[0]

        self.assertEqual(test_tag.tag_name, test_tip_tag.tag.tag_name)

    def test_tip_tag_to_tip_query(self):
        """Test that query functionality between tip_tag and tip objects is working properly"""

        test_tip = seed_database.tips_in_db[2]
        test_tip_tag = seed_database.tip_tags_in_db[2]

        self.assertEqual(test_tip.tip_text, test_tip_tag.tip.tip_text)

if __name__ == "__main__":
    unittest.main()