"""Tests to ensure model.py user table is functioning propery"""

import unittest
import os

from server import app
import crud
import model

os.system('dropdb travel_project')
os.system('createdb travel_project')


class UserTestCase(unittest.TestCase):
    """Tests for User table in model"""

    def setUp(self):
        print("********* User setUp function is running **************")
        model.connect_to_db(app)
        model.db.create_all()

    def test_user_exists(self):
        """Test that a user is in users table after adding to db.session"""
        test_user = crud.create_user(username="buttersnaps", fname="Ghee", lname="Buttersnaps",
                                            email = "gbutter@me.com", password="123441")
        model.db.session.add(test_user)
        model.db.session.commit()
        test_query = model.User.query.filter(model.User.fname == test_user.fname).first()
        self.assertEqual(test_user, test_query)
    
    def test_get_all_users(self):
        """Test that CRUD function returns a list of all users"""

        all_users = model.User.query.all()
        crud_all_users = crud.show_users()
        self.assertEqual(all_users, crud_all_users)

    def test_get_user_by_id(self):
        """Test that CRUD function returns the correct user"""

        test_user = model.User.query.filter(model.User.user_id == '1').first()
        crud_user = crud.get_user_by_id(user_id='1')
        self.assertEqual(test_user, crud_user)
    
    def test_get_user_by_email(self):
        """Test that CRUD function returns the correct user"""

        test_user = model.User.query.filter(model.User.email == 'gbutter@me.com').first()
        crud_user = crud.get_user_by_email(email='gbutter@me.com')
        self.assertEqual(test_user, crud_user)
    
    def test_get_user_by_fname(self):
        """Test that CRUD function return the correct user"""

        test_user = model.User.query.filter(model.User.fname == 'Ghee').first()
        crud_user = crud.get_user_by_fname(fname = 'Ghee')
        self.assertEqual(test_user, crud_user)

    def test_user_travel_relationship(self):
        """Test that the user is successfully related to travels table"""

        test_travel = crud.create_travel(departure_date="2021.10.05", arrival_date="2021.10.15")
        test_user = crud.create_user_with_travel_id(username='tapman', fname='Burton', lname='Guster', 
                                email='guster@me.com', password='goawayshawn', travel_id = test_travel.travel_id)
        
        self.assertFalse(test_user.travel_id == None)
        self.assertFalse(test_user.travel.arrival_date == None)

if __name__ == "__main__":
    unittest.main()