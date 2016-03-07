import unittest 
from unittest import TestCase
from server import app
from model import User, Input, Recipe 
from datetime import date 
import server 

# First, will test graph implementations. 
class GraphCalculations(TestCase):
	"""Unit tests for making the correct calculations on my graph"""

	def setUp(self):
    """Stuff to do before every test."""
    self.client = app.test_client()
    app.config['TESTING'] = True

		# connecting to test database. 
		connect_to_db(app, "postgresql:///testdb")

		db.create_all()


	def tearDown(self):
    """Do at end of every test."""

    db.session.close()
    db.drop_all()

  def calculate_recipe_totals(self):
    """A test returning the recipe totals."""
    
     

    self.assertEqual("")

  		

  def calculate_recipes(self, (datetime.date(2015, 03, 04))):
    """Calculating recipes"""


  	result = self.client.get('/')
