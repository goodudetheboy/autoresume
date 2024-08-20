import unittest

import yaml

from content.answer import *


class AnswerTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_answer_app_question(self):
        """
        Test the main function to answer app question based on resume and job description
        """
        with open("./tests/data/test_resume.yaml", 'r') as file:
            resume = yaml.safe_load(file)

        with open("./tests/data/test_app_question.txt", 'r') as file:
            test_question = file.read()

        with open("./tests/data/test_job_description.txt", "r") as file:
            job_description = file.read()

        result_json, actual_prompt = answer_app_question(
            test_question, resume, job_description)

        with open("./tests/data/test_app_question_expected.txt", "r") as file:
            expected_prompt = file.read()

        self.assertEqual(actual_prompt, expected_prompt)

        self.assertIn("analysis", result_json)
        self.assertIn("answer", result_json)
