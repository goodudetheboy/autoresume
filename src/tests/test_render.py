import yaml
import unittest
from content.render import render_yaml_to_latex

class ContentToResumeTest(unittest.TestCase):
	def test_yaml_to_latex_test(self):
		with open("./data/test_tailored.yaml", 'r') as file:
			data = yaml.safe_load(file)

		with open("./data/test_tailored.tex", 'r') as file:
			expected_latex = file.read()

		actual_latex = render_yaml_to_latex(data)

		self.assertEquals(actual_latex, expected_latex)