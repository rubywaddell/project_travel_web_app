"""Tests to insure model.py is functioning propery"""

import unittest

from server import app

import crud

import os

os.system('dropdb travel_project')
os.system('createdb travel_project')

class UserTestCase(unittest.TestCase):
    """Tests for User table in model"""

    def setUp(self):
        print("********* User setUp function is running **************")
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
    
    def test_travel_relationship(self):
        """Test that the user is successfully related to travels table"""
        test_travel = crud.model.Travel.query.first()
        test_user = crud.create_user_with_travel_id(username='tapman', fname='Burton', lname='Guster', 
                                email='guster@me.com', password='goawayshawn', travel_id = test_travel.travel_id)
        
        self.assertFalse(test_user.travel_id == None)
        self.assertFalse(test_user.travel.arrival_date == None)


class TravelTestCase(unittest.TestCase):
    """Tests for Travel table in model"""

    def setUp(self):
        print("********* Travel setUp function is running **************")
        crud.model.connect_to_db(app)
        crud.model.db.create_all()

    def test_travel_exists(self):
        """Test that a trip is in travels table after adding to db.session"""
        test_travel = crud.create_travel(departure_date="10.05.2021", arrival_date="10.10.2021")
        crud.model.db.session.add(test_travel)
        crud.model.db.session.commit()
        test_query = crud.model.Travel.query.filter(crud.model.Travel.arrival_date == test_travel.arrival_date).first()
        self.assertEqual(test_travel, test_query)


class StateTestCase(unittest.TestCase):
    """Tests for State table in database"""

    def setUp(self):
        print("********* State setUp function is running **************")
        crud.model.connect_to_db(app)
        crud.model.db.create_all()

    def test_state_exists(self):
        """Test that a state is in the states table after adding to db.session"""
        test_state = crud.create_state(state_name="Narnia")
        crud.model.db.session.add(test_state)
        crud.model.db.session.commit()
        test_query = crud.model.State.query.filter(crud.model.State.state_name == test_state.state_name).first()
        self.assertEqual(test_state, test_query)


if __name__ == "__main__":
    unittest.main()


os.system('dropdb travel_project')