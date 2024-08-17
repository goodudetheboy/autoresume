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

        expected_response = {'details': [{'loc': ['phone'], 'msg': 'Field required'},
                                         {'loc': ['email'],
                                          'msg': 'Field required'},
                                         {'loc': ['website'],
                                          'msg': 'Field required'},
                                         {'loc': ['linkedin'],
                                          'msg': 'Field required'},
                                         {'loc': ['github'],
                                          'msg': 'Field required'},
                                         {'loc': ['education_list'],
                                          'msg': 'Field required'},
                                         {'loc': ['skills'],
                                          'msg': 'Field required'},
                                         {'loc': ['experience_list'],
                                          'msg': 'Field required'},
                                         {'loc': ['project_list'],
                                          'msg': 'Field required'},
                                         {'loc': ['awards_list'], 'msg': 'Field required'}],
                             'error': 'Schema validation failed',
                             'result': 'invalid'}
        self.assertEqual(response.get_json(), expected_response)

    def test_post_validate_resume_missing_fields(self):
        json_payload = {}

        response = self.app.post("/api/resume/validate", json=json_payload)

        self.assertEqual(response.status_code, 400)

        expected_response = {
            "error": "No resume provided"
        }
        self.assertEqual(response.get_json(), expected_response)
