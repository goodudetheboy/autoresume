import unittest
from app import app


class IndexPageTest(unittest.TestCase):
    def setUp(self):
        # Set up a test client for the Flask application
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test the index route '/' to ensure it loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Original', response.data)
        self.assertIn(b'Tailored', response.data)
