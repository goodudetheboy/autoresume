import yaml
import unittest
from content.render import *

class ContentToResumeTest(unittest.TestCase):
	def setUp(self):
		self.maxDiff = None

	def test_data_to_latex(self):
		with open("./tests/data/test_tailored.yaml", 'r') as file:
			data = yaml.safe_load(file)

		with open("./tests/data/test_tailored.tex", 'r') as file:
			expected_latex = file.read()

		actual_latex = render_data_to_latex(data)
		self.assertEqual(expected_latex, actual_latex)

	def test_yaml_file_to_latex_file(self):

		read_yaml_and_write_latex("./tests/data/test_tailored.yaml", "./tests/data/actual_tailored.tex")

		with open("./tests/data/test_tailored.tex", 'r') as file:
			expected_latex = file.read()
		
		with open("./tests/data/actual_tailored.tex", 'r') as file:
			actual_latex = file.read()
	
		self.assertEqual(expected_latex, actual_latex)