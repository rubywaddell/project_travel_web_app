"""Tests to insure model.py is functioning propery"""

from unittest import TestCase

# from server import app

import model

def create_test_user():
    """Create a test User """
    user_name = "inapanic"
    full_name = "Peter Panics"
    email = "peterpanics@gmail.com"
    password = "panicking4ever"

    test_user = model.User(user_name, full_name, email, password)

    return test_user