import unittest
from app import app


class ResumeAPITestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client
        self.app = app.test_client()
        self.app.testing = True
        self.maxDiff = None

    def test_post_validate_resume(self):
        with open("./tests/data/test_resume.yaml", "r") as resume_file:
            resume_yaml = resume_file.read()
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
            "resume": "name: Vuong Ho",
        }

        response = self.app.post("/api/resume/validate", json=json_payload)

        self.assertEqual(response.status_code, 200)

        expected_response = {"details": [
            "Problem at [phone] with error [Field required]",
            "Problem at [email] with error [Field required]",
            "Problem at [website] with error [Field required]",
            "Problem at [linkedin] with error [Field required]",
            "Problem at [github] with error [Field required]",
            "Problem at [education_list] with error [Field required]",
            "Problem at [skills] with error [Field required]",
            "Problem at [experience_list] with error [Field required]",
            "Problem at [project_list] with error [Field required]",
            "Problem at [awards_list] with error [Field required]"
        ],
            "error": "Schema validation failed",
            "result": "invalid"
        }
        self.assertEqual(response.get_json(), expected_response)

    def test_post_validate_resume_missing_fields(self):
        json_payload = {}

        response = self.app.post("/api/resume/validate", json=json_payload)

        self.assertEqual(response.status_code, 400)

        expected_response = {
            "error": "No resume provided"
        }
        self.assertEqual(response.get_json(), expected_response)

    def test_post_render_resume(self):
        with open("./tests/data/test_resume.yaml", "r") as resume_file:
            resume_yaml = resume_file.read()
        json_payload = {
            "resume": resume_yaml,
        }

        response = self.app.post("/api/resume/render", json=json_payload)
        self.assertEqual(response.status_code, 200)

    def test_post_render_resume_invalid(self):
        json_payload = {
            "resume": "name: Vuong Ho",
        }

        response = self.app.post("/api/resume/render", json=json_payload)

        self.assertEqual(response.status_code, 200)
        expected_response = {
            "result": "valid"
        }

        expected_response = {"details": [
            "Problem at [phone] with error [Field required]",
            "Problem at [email] with error [Field required]",
            "Problem at [website] with error [Field required]",
            "Problem at [linkedin] with error [Field required]",
            "Problem at [github] with error [Field required]",
            "Problem at [education_list] with error [Field required]",
            "Problem at [skills] with error [Field required]",
            "Problem at [experience_list] with error [Field required]",
            "Problem at [project_list] with error [Field required]",
            "Problem at [awards_list] with error [Field required]"
        ],
            "error": "Schema validation failed",
            "result": "invalid"
        }
        self.assertEqual(response.get_json(), expected_response)
