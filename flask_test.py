import unittest 
import doctest 
import server
from unittest import TestCase
from server import app
from model import User, Input, Recipe, connect_to_db, db
from datetime import date 
import flask 
from server import calculate_recipe_totals
 

# First, will test graph implementations. 
class GraphCalculations(TestCase):
  """Unit tests for making the correct calculations on my graph"""

  def setUp(self):
    """Stuff to do before every test."""
    self.client = app.test_client()

    with self.client as c:
      with c.session_transaction() as s:
        s["user_id"] = 1


    app.config['TESTING'] = True

    # connecting to test database. 
    connect_to_db(app, 'postgresql:///testdb')

    db.create_all()

  def test_calculate_recipe_totals_for_user_id_1(self):
    """A test returning the recipe totals."""


    results = self.client.get('/calculate-recipe-totals')

    self.assertIn('d_total_fat = [87.21399872334617, 188.53615655608982, 32.13505666666669, 366.99382250971775, 119.90530117466679]', results.data )
    self.assertIn('d_total_protein = [63.087606135, 106.32030300041666, 18.27962454666667, 130.2912317318333, 104.1618023604]', results.data)
    self.assertIn('d_total_fat = [87.21399872334617, 188.53615655608982, 32.13505666666669, 366.99382250971775, 119.90530117466679]', results.data)
    self.assertIn('data_list = ["02/29", "03/01", "03/02", "03/03", "03/04"]', results.data)
    self.assertIn('text/html', results.headers['Content-Type'])
    self.assertEqual(results.status_code, 200)


  def test_calculate_recipes_march_04(self):
    """Test calculating recipes on the 4th of March"""

    results = self.client.get('/calculate-recipes/2016-03-04')

    self.assertIn('data = "{\\"total_fat\\": \\"119.91\\", \\"total_protein\\": \\"104.16\\", \\"total_carbs\\": \\"81.46\\"}"', results.data)
    self.assertIn('text/html', results.headers['Content-Type'])
    self.assertEqual(results.status_code, 200)


  def test_process_recipe_info(self):

    results = self.client.get('/recipe/input/guacamole')

    self.assertIn('data = "{\\"percentage_of_carbs\\": \\"4.26\\", \\"percentage_of_fat\\": \\"22.78\\", \\"percentage_of_protein\\": \\"5.09\\"}"', results.data)
    self.assertIn('text/html', results.headers['Content-Type'])
    self.assertEqual(results.status_code, 200)

  def test_redirect_calculate_recipes(self):

    results = self.client.get('redirect-calculate-recipes/date?date=2016-03-04')

    self.assertEqual(results.status_code, 302)

  def test_redirect_error(self):

    results = self.client.get('/error')

    self.assertIn('<h1>No vegan dishes were found for one (or more) of your entries!</h1>', results.data)

  def test_show_recipes_date(self):

    results = self.client.get('/show_recipes_date/date/?date=2016-03-04')

    self.assertIn('\t\t\t\t\tRava Dosa With Potato Chickpea Masala     \n \t\t\t\t', results.data)
    self.assertIn('\n \t\t\t\t\tRava Dosa With Potato Chickpea Masala     \n \t\t\t\t', results.data)
    self.assertIn('\n \t\t\t\t\tChile Peanuts     \n \t\t\t\t', results.data)

  def test_dish_directory(self):

    results = self.client.get('/dish-directory')

    self.assertIn('\n \t\t\t\t\tAlmond Butter Oatmeal\n\n \t\t\t\t', results.data)
    self.assertIn('\n \t\t\t\t\tBanana &amp; Almond Butter Toast\n\n \t\t\t\t', results.data)
    self.assertIn('\n \t\t\t\t\tBraised Eggplant With Garlic And Basil\n\n \t\t\t\t', results.data)
    self.assertIn('\n \t\t\t\t\tCherry Vanilla Almond Smoothie\n\n \t\t\t\t', results.data)
    self.assertIn('\n \t\t\t\t\tChile Peanuts\n\n \t\t\t\t', results.data)







  # 

#     result = self.client.get('/')

# class IntegrationTestCase(TestCase):
#   """Integration Tests for the flask server"""

#   def setUp(self):
#     """Do before every test"""

#     # Get the Flask test client
#     self.client = app.test_client()

#     # Show Flask errors that happen during tests
#     app.config['TESTING'] = True

#     # Connect to test database
#     connect_to_db(app, "postgresql:///testdb")
#     db.create_all()

#   def tearDown(self):
#     """Do at end of every test."""

#     db.session.close()
#     db.drop_all()

#   def test_homepage(self):
#     """Tests result of homepage."""

#     result = self.client.get("/")
#     self.assertEqual(result.status_code, 200)
#     self.assertIn('text/html', result.headers['Content-Type'])

#   def test_user(self):
#     """Test the user page"""

#     result = self.client.get("/user")

    # self.assertEqual(result.status_code, 302)


if __name__ == '__main__':
  unittest.main()

