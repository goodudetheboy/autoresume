import unittest
import yaml
from content.tailor import *

class TailorResumeTest(unittest.TestCase):
	def test_tailor_resume(self):
		with open("./tests/data/test_raw.yaml", 'r') as file:
			data = yaml.safe_load(file)

		with open("./tests/data/test_job_description.txt", "r") as file:
			jd = file.read()

		result = tailor_resume_by_job_description(data, jd)

		self.assertIn("keywords", result)
		self.assertIn("resume", result)

		self.assertIsNotNone(result)