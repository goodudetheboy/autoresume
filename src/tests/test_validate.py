import unittest
import yaml
from content.validate import *


class ValidateResumeTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_validate_resume_valid(self):
        with open("./tests/data/test_resume.yaml", 'r') as file:
            data = file.read()

        result, errors = validate_resume(data)

        self.assertTrue(result)
        self.assertIsNone(errors)

    def test_validate_resume_invalid(self):
        result, actual_errors = validate_resume("name: Vuong Ho")

        self.assertFalse(result)

        expected_errors = {"details": [
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
        }

        self.assertEqual(actual_errors, expected_errors)
