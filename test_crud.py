"""Tests to insure model.py is functioning propery"""

import unittest
import os

from server import app
import crud
import model

os.system('dropdb travel_project')
os.system('createdb travel_project')

class StateTestCase(unittest.TestCase):
    """Tests for State table in database"""

    def setUp(self):
        print("********* State setUp function is running **************")
        model.connect_to_db(app)
        model.db.create_all()

    def test_state_exists(self):
        """Test that a state is in the states table after adding to db.session"""
        test_state = crud.create_state(state_name="Narnia")
        model.db.session.add(test_state)
        model.db.session.commit()
        test_query = model.State.query.filter(model.State.state_name == test_state.state_name).first()
        self.assertEqual(test_state, test_query)

    def test_get_state_by_state_name(self):
        """Test that CRUD function returns the correct state object with given name"""

        test_state = model.State.query.filter(model.State.state_name == 'Narnia').first()
        crud_state = crud.get_state_by_state_name(state_name = 'Narnia')
        self.assertEqual(test_state, crud_state)

class CityTestCase(unittest.TestCase):
    """Tests for City table in database"""

    def setUp(self):
        print("********* City setUp function is running **************")
        model.connect_to_db(app)
        model.db.create_all()

    def test_city_exists(self):
        """Test that a city is in the cities table after adding to db.session"""
        test_city = crud.create_city(city_name="Oz")
        model.db.session.add(test_city)
        model.db.session.commit()
        test_query = model.City.query.filter(model.City.city_name == test_city.city_name).first()
        self.assertEqual(test_city, test_query)

    def test_get_city_by_city_name(self):
        """Test that CRUD function returns the correct city object with given name"""

        test_city = model.City.query.filter(model.City.city_name == 'Oz').first()
        crud_city = crud.get_city_by_city_name(city_name = 'Oz')
        self.assertEqual(test_city, crud_city)

    def test_city_state_relationship(self):
        """Test that a city object is successfuly connected to the states table"""

        test_state = crud.create_state(state_name="Hogwarts")
        test_city = model.City(city_name="Oz", state_id=test_state.state_id)
        model.db.session.add(test_city)
        model.db.session.commit()

        self.assertFalse(test_city.state_id == None)
        self.assertFalse(test_city.state.state_name == None)


class TipTestCase(unittest.TestCase):
    """Tests for the Tips table in database"""

    def setUp(self):
        print("********* Tip setUp function is running **************")
        model.connect_to_db(app)
        model.db.create_all()    

    def test_tip_exists(self):
        """Test that a tip is in the tips table after adding to db.session"""
        test_tip = crud.create_tip(tip_text="Watch out for pickpockets!")
        model.db.session.add(test_tip)
        model.db.session.commit()
        test_query = model.Tip.query.filter(model.Tip.tip_text == test_tip.tip_text).first()
        self.assertEqual(test_tip, test_query)

    # def test_tip_state_relationship(self):
    #     """Test that a tip object is successfuly connected to the states table"""

    #     test_state = model.State.query.first()
    #     test_tip = model.Tip(tip_text="Don't go out alone at night if you're travelling alone.", state_id=test_state.state_id)
    #     model.db.session.add(test_tip)
    #     model.db.session.commit()

    #     self.assertFalse(test_tip.state_id == None)
    #     self.assertFalse(test_tip.state.state_name == None)


class TipTagTestCase(unittest.TestCase):
    """Tests for the TipTags table in database"""

    def setUp(self):
        print("********* TipTag setUp function is running **************")
        model.connect_to_db(app)
        model.db.create_all()    

    def test_tip_tag_exists(self):
        """Test that a tip_tag is in the tiptags table after adding to db.session"""

        test_tip_tag = crud.create_tip_tag()

        model.db.session.add(test_tip_tag)
        model.db.session.commit()

        test_query = model.TipTag.query.filter(model.TipTag.tip_tag_id == test_tip_tag.tip_tag_id).first()
        self.assertEqual(test_tip_tag, test_query)
    

    def test_tip_tag_tip_relationship(self):
        """Test that a tiptag object is successfuly connected to the tips table"""

        test_tip = crud.create_tip(tip_text="this is a test")

        print()
        print("*"*35)
        print("test_tip=", test_tip)
        print("*"*35)
        print()

        test_tip_tag = model.TipTag(tip_id = test_tip.tip_id)

        model.db.session.add(test_tip_tag)
        model.db.session.commit()

        self.assertFalse(test_tip_tag.tip_id == None)
        self.assertFalse(test_tip_tag.tip.tip_text == None)

    def test_tip_tag_tag_relationship(self):
        """Test that a tiptag object is successfully connected to the tags table"""

        test_tag = model.Tag.query.first()

        test_tip_tag = model.TipTag(tag_id = test_tag.tag_id)
        model.db.session.add(test_tip_tag)
        model.db.session.commit()

        self.assertFalse(test_tip_tag.tag_id == None)
        self.assertFalse(test_tip_tag.tag.tag_name == None)


class TagTestCase(unittest.TestCase):
    """Tests for the Tags table in database"""

    def setUp(self):
        print("********* Tag setUp function is running **********\n")
        model.connect_to_db(app)
        model.db.create_all()
    
    def test_tag_exists(self):
        """Test that a tag is in the tags table after adding to db.session"""

        test_tag = crud.create_tag(tag_name="Vegetarian")

        model.db.session.add(test_tag)
        model.db.session.commit()

        test_query = model.Tag.query.filter(model.Tag.tag_name == test_tag.tag_name).first()
        self.assertEqual(test_tag, test_query)


if __name__ == "__main__":
    unittest.main()