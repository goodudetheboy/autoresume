import unittest
from app import app


class ResumeAPITestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client
        self.app = app.test_client()
        self.app.testing = True

    def test_post_validate_resume(self):
        with open("../data/test_resume.yaml", "r") as resume_file:
            resume_yaml = resume_file
        json_payload = {
            "resume": resume_yaml,
        }

        response = self.app.post("/api/resume/validate", json=json_payload)

        self.assertEqual(response.status_code, 200)

        expected_response = {
            "result": "valid"
        }
        self.assertEqual(response.get_json(), expected_response)

    def test_post_validate_resume_invalid(self):
        json_payload = {
            "resume": "fasdfpasdfj;4209vn4098n[Garbled bullshit]",
        }

        response = self.app.post("/api/resume/validate", json=json_payload)

        self.assertEqual(response.status_code, 200)

        expected_response = {
            "result": "invalid"
        }
        self.assertEqual(response.get_json(), expected_response)

    def test_post_validate_resume_missing_fields(self):
        json_payload = {}

        response = self.app.post("/api/resume/validate", json=json_payload)

        self.assertEqual(response.status_code, 400)

        expected_response = {
            "error": "Missing fields"
        }
        self.assertEqual(response.get_json(), expected_response)
