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
    
    def test_user_travel_relationship(self):
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


    def test_travel_state_relationship(self):
        """Test that a trip object is successfuly connected to the states table"""

        test_state = crud.model.State.query.first()
        test_travel = crud.model.Travel(departure_date="12.24.2010", arrival_date="12.26.2015", state_id=test_state.state_id)
        crud.model.db.session.add(test_travel)
        crud.model.db.session.commit()

        self.assertFalse(test_travel.state_id == None)
        self.assertFalse(test_travel.state.state_name == None)


    def test_travel_city_relationship(self):
        """Test that a trip object is successfully connected to the states table"""

        test_city = crud.model.City.query.first()
        test_travel = crud.model.Travel(departure_date="12.26.2015", arrival_date="12.24.2010", city_id=test_city.city_id)
        crud.model.db.session.add(test_travel)
        crud.model.db.session.commit()

        self.assertFalse(test_travel.city_id == None)
        self.assertFalse(test_travel.city.city_name == None)


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


class CityTestCase(unittest.TestCase):
    """Tests for City table in database"""

    def setUp(self):
        print("********* City setUp function is running **************")
        crud.model.connect_to_db(app)
        crud.model.db.create_all()

    def test_city_exists(self):
        """Test that a city is in the cities table after adding to db.session"""
        test_city = crud.create_city(city_name="Oz")
        crud.model.db.session.add(test_city)
        crud.model.db.session.commit()
        test_query = crud.model.City.query.filter(crud.model.City.city_name == test_city.city_name).first()
        self.assertEqual(test_city, test_query)


class TipTestCase(unittest.TestCase):
    """Tests for the Tips table in database"""

    def setUp(self):
        print("********* Tip setUp function is running **************")
        crud.model.connect_to_db(app)
        crud.model.db.create_all()    

    def test_tip_exists(self):
        """Test that a tip is in the tips table after adding to db.session"""
        test_tip = crud.create_tip(tip_text="Watch out for pickpockets!")
        crud.model.db.session.add(test_tip)
        crud.model.db.session.commit()
        test_query = crud.model.Tip.query.filter(crud.model.Tip.tip_text == test_tip.tip_text).first()
        self.assertEqual(test_tip, test_query)

    # def test_tip_state_relationship(self):
    #     """Test that a tip object is successfuly connected to the states table"""

    #     test_state = crud.model.State.query.first()
    #     test_tip = crud.model.Tip(tip_text="Don't go out alone at night if you're travelling alone.", state_id=test_state.state_id)
    #     crud.model.db.session.add(test_tip)
    #     crud.model.db.session.commit()

    #     self.assertFalse(test_tip.state_id == None)
    #     self.assertFalse(test_tip.state.state_name == None)


class TipTagTestCase(unittest.TestCase):
    """Tests for the TipTags table in database"""

    def setUp(self):
        print("********* TipTag setUp function is running **************")
        crud.model.connect_to_db(app)
        crud.model.db.create_all()    

    def test_tip_tag_exists(self):
        """Test that a tip_tag is in the tiptags table after adding to db.session"""

        test_tip_tag = crud.create_tip_tag()

        crud.model.db.session.add(test_tip_tag)
        crud.model.db.session.commit()

        test_query = crud.model.TipTag.query.filter(crud.model.TipTag.tip_tag_id == test_tip_tag.tip_tag_id).first()
        self.assertEqual(test_tip_tag, test_query)
    

    def test_tip_tag_tip_relationship(self):
        """Test that a tiptag object is successfuly connected to the tips table"""

        test_tip = crud.create_tip(tip_text="this is a test")

        print()
        print("*"*35)
        print("test_tip=", test_tip)
        print("*"*35)
        print()

        test_tip_tag = crud.model.TipTag(tip_id = test_tip.tip_id)

        crud.model.db.session.add(test_tip_tag)
        crud.model.db.session.commit()

        self.assertFalse(test_tip_tag.tip_id == None)
        self.assertFalse(test_tip_tag.tip.tip_text == None)


class TagTestCase(unittest.TestCase):
    """Tests for the Tags table in database"""

    def setUp(self):
        print("********* Tag setUp function is running **********\n")
        crud.model.connect_to_db(app)
        crud.model.db.create_all()
    
    def test_tag_exists(self):
        """Test that a tag is in the tags table after adding to db.session"""

        test_tag = crud.create_tag(tag_name="Vegetarian")

        crud.model.db.session.add(test_tag)
        crud.model.db.session.commit()

        test_query = crud.model.Tag.query.filter(crud.model.Tag.tag_name == test_tag.tag_name).first()
        self.assertEqual(test_tag, test_query)


if __name__ == "__main__":
    unittest.main()