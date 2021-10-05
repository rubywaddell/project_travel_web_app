"""Tests to insure model.py is functioning propery"""

import unittest

from server import app

import crud


class UserTestCase(unittest.TestCase):
    """Tests for User table in model"""

    def setUp(self):
        print("********* setUp function is running **************")
        crud.model.connect_to_db(app)
        crud.model.db.create_all()
    
    def create_test_user(self):
        """Create a test User """

        user_name = "inapanic"
        full_name = "Peter Panics"
        email = "peterpanics@gmail.com"
        password = "panicking4ever"

        test_user = crud.model.User(username=user_name, full_name=full_name, email=email, password=password)

        return test_user

    def test_user_exists(self):
        """Test that a user is in users table after adding to db.session"""
        test_user = crud.create_user(username="buttersnaps", fname="Ghee", lname="Buttersnaps",
                                            email = "gbutter@me.com", password="123441")
        crud.model.db.session.add(test_user)
        crud.model.db.session.commit()
        test_query = crud.model.User.query.filter(crud.model.User.fname == test_user.fname).first()
        self.assertEqual(test_user, test_query)

    def tearDown(self):
        # crud.model.db.
        pass


if __name__ == "__main__":
    unittest.main()
