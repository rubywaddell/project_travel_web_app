"""Tests to ensure model.py travel table is functioning propery"""

import unittest
import os

from server import app
import crud
import model

os.system('dropdb travel_project')
os.system('createdb travel_project')


class TravelTestCase(unittest.TestCase):
    """Tests for Travel table in model"""

    def setUp(self):
        print("********* Travel setUp function is running **************")
        model.connect_to_db(app)
        model.db.create_all()

    def test_travel_exists(self):
        """Test that a trip is in travels table after adding to db.session"""
        test_travel = crud.create_travel(departure_date="10.05.2021", arrival_date="10.10.2021")
        model.db.session.add(test_travel)
        model.db.session.commit()
        test_query = model.Travel.query.filter(model.Travel.arrival_date == test_travel.arrival_date).first()
        self.assertEqual(test_travel, test_query)

    def test_get_all_travels(self):
        """Test that CRUD function returns a list of all travels"""

        all_travels = model.Travel.query.all()
        crud_all_travels = crud.show_travels()
        self.assertEqual(all_travels, crud_all_travels)
    
    def test_get_travel_by_departure_date(self):
        """Test that CRUD function returns the correct travel object"""

        test_travel = model.Travel.query.filter(model.Travel.departure_date == '10.05.2021').first()
        crud_travel = crud.get_travel_by_departure_date(departure_date = '10.05.2021')
        self.assertEqual(test_travel, crud_travel)

    def test_travel_state_relationship(self):
        """Test that a trip object is successfuly connected to the states table"""

        test_state = crud.create_state(state_name="Portlandia")
        test_travel = model.Travel(departure_date="12.24.2010", arrival_date="12.26.2015", state_id=test_state.state_id)
        model.db.session.add(test_travel)
        model.db.session.commit()

        self.assertFalse(test_travel.state_id == None)
        self.assertFalse(test_travel.state.state_name == None)

    # def test_travel_city_relationship(self):
    #     """Test that a trip object is successfully connected to the states table"""

    #     test_city = model.City.query.first()
    #     test_travel = model.Travel(departure_date="12.26.2015", arrival_date="12.24.2010", city_id=test_city.city_id)
    #     model.db.session.add(test_travel)
    #     model.db.session.commit()

    #     self.assertFalse(test_travel.city_id == None)
    #     self.assertFalse(test_travel.city.city_name == None)


if __name__ == "__main__":
    unittest.main()