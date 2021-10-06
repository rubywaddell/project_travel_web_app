"""Tests to ensure model.py State and City tables are functioning propery"""

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

if __name__ == "__main__":
    unittest.main()