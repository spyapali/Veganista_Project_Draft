import unittest 
import doctest 
import server
from unittest import TestCase
from server import app
from model import User, Input, Recipe, connect_to_db, db
from datetime import date 
from server import calculate_recipe_totals
 

# First, will test graph implementations. 
class GraphCalculations(TestCase):
  """Unit tests for making the correct calculations on my graph"""

  def setUp(self):
    """Stuff to do before every test."""
    self.client = app.test_client()
    app.config['TESTING'] = True

    # connecting to test database. 
    connect_to_db(app, 'postgresql:///testdb')

    db.create_all()

  def tearDown(self):
    """Do at end of every test."""

    db.session.close()
    db.drop_all()

  def test_calculate_recipe_totals_for_user_id_1(self):
    """A test returning the recipe totals."""

    with app.test_client() as c:
      with c.session_transaction() as sess:
        sess['user_id'] = 1


    calculate_recipe_totals()

    self.assertEqual(date_list, [datetime.date(2016, 2, 29), datetime.date(2016, 3, 1), datetime.date(2016, 3, 2), datetime.date(2016, 3, 3), datetime.date(2016, 3, 4)])

#   def test_calculate_recipes_march_04(self, (datetime.date(2015, 03, 04))):
#     """Calculating recipes"""

#     assert flask.session['user_id'] == 1




#   	result = self.client.get('/')

class IntegrationTestCase(TestCase):
  """Integration Tests for the flask server"""

  def setUp(self):
    """Do before every test"""

    # Get the Flask test client
    self.client = app.test_client()

    # Show Flask errors that happen during tests
    app.config['TESTING'] = True

    # Connect to test database
    connect_to_db(app, "postgresql:///testdb")
    db.create_all()

  def tearDown(self):
    """Do at end of every test."""

    db.session.close()
    db.drop_all()

  def test_homepage(self):
    """Tests result of homepage."""

    result = self.client.get("/")
    self.assertEqual(result.status_code, 200)
    self.assertIn('text/html', result.headers['Content-Type'])

  def test_user(self):
    """Test the user page"""

    result = self.client.get("/user")

    self.assertEqual(result.status_code, )


if __name__ == '__main__':
  unittest.main()


