import unittest
import yaml

from app import app
from unittest.mock import patch


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

        self.assertEqual(response.status_code, 201)

    def test_post_render_resume_invalid(self):
        json_payload = {
            "resume": "name: Vuong Ho",
        }

        response = self.app.post("/api/resume/render", json=json_payload)

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

    def test_post_tailor_resume_valid(self):
        with open("./tests/data/test_resume.yaml", "r") as resume_file:
            resume_yaml = resume_file.read()
        with open("./tests/data/test_job_description.txt", "r") as jd_file:
            job_description = jd_file.read()
        json_payload = {
            "resume": resume_yaml,
            "job_description": job_description
        }

        response = self.app.post("/api/resume/tailor", json=json_payload)

        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertIn("tailored_resume", response_json)
        self.assertIn("keywords", response_json)

        self.assertTrue(yaml.safe_load(response_json["tailored_resume"]))

    def test_post_tailor_resume_missing_fields(self):
        json_payload = {
            "resume": "name: Vuong Ho",
        }

        response = self.app.post("/api/resume/tailor", json=json_payload)

        self.assertEqual(response.status_code, 400)

        expected_response = {
            "error": "Missing job description"
        }

        self.assertEqual(response.get_json(), expected_response)

    @patch("app.answer_app_question")
    def test_post_answer_app_question(self, mock_answer_app_question):
        """Test /api/resume/answer (anwer app question) endpoint """

        json_payload = {
            "resume": "name: Vuong Ho",
            "job_description": "Job Description",
            "question": "Question here"
        }

        mock_analysis = "Analysis here"
        mock_answer = "Answer here"
        mock_prompt = "Prompt here"

        mock_answer_app_question.return_value = (
            {
                "analysis": mock_analysis,
                "answer": mock_answer,
            },
            mock_prompt)

        response = self.app.post("/api/resume/answer", json=json_payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "analysis": mock_analysis,
            "answer": mock_answer,
            "prompt": mock_prompt
        })
