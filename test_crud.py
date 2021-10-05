"""Tests to insure model.py is functioning propery"""

import unittest

from server import app

import crud

import os

class UserTestCase(unittest.TestCase):
    """Tests for User table in model"""

    def setUp(self):
        print("********* setUp function is running **************")
        os.system('dropdb travel_project')
        os.system('createdb travel_project')
        crud.model.connect_to_db(app)
        crud.model.db.create_all()

    def test_user_exists(self):
        """Test that a user is in users table after adding to db.session"""
        test_user = crud.create_user(username="buttersnaps", fname="Ghee", lname="Buttersnaps",
                                            email = "gbutter@me.com", password="123441")
        crud.model.db.session.add(test_user)
        crud.model.db.session.commit()
        test_query = crud.model.User.query.filter(crud.model.User.fname == test_user.fname).first()
        self.assertEqual(test_user, test_query)

    def tearDown(self):
        os.system('dropdb travel_project')
        # os.system('createdb travel_project')


class TravelTestCase(unittest.TestCase):
    """Tests for Travel table in model"""

    def setUp(self):
        print("********* setUp function is running **************")
        os.system('dropdb travel_project')
        os.system('createdb travel_project')
        crud.model.connect_to_db(app)
        crud.model.db.create_all()

    def test_travel_exists(self):
        """Test that a trip is in travels table after adding to db.session"""
        test_travel = crud.create_travel(departure_date="10.05.2021", arrival_date="10.10.2021")
        crud.model.db.session.add(test_travel)
        crud.model.db.session.commit()
        test_query = crud.model.Travel.query.filter(crud.model.Travel.arrival_date == test_travel.arrival_date).first()
        self.assertEqual(test_travel, test_query)

    def tearDown(self):
        os.system('dropdb travel_project')
        # os.system('createdb travel_project')



if __name__ == "__main__":
    unittest.main()
