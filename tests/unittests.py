from unittest import TestCase
from server import app

class FlaskTests(TestCase):

  def setUp(self):
      """Stuff to do before every test."""

      self.client = app.test_client()
      app.config['TESTING'] = True

  def test_process_user_login(self):
      """Some non-database test..."""

      result = self.client.get("/process-login")
	