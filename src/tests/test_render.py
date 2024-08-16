import yaml
import os
import subprocess
import unittest

from content.render import *

class RenderTest(unittest.TestCase):
	def setUp(self):
		self.maxDiff = None

	def test_data_to_latex(self):
		with open("./tests/data/test_resume.yaml", 'r') as file:
			data = yaml.safe_load(file)

		with open("./tests/data/test_tailored.tex", 'r') as file:
			expected_latex = file.read()

		actual_latex = render_data(data)
		self.assertEqual(expected_latex, actual_latex)

	def test_yaml_file_to_latex_file(self):
		
		expected_path = os.path.abspath("./tests/data/actual_tailored.tex")
		actual_path = read_yaml_and_write_latex("./tests/data/test_resume.yaml", "./tests/data/actual_tailored.tex")

		self.assertEqual(expected_path, actual_path)

		with open("./tests/data/test_tailored.tex", 'r') as file:
			expected_latex = file.read()
		
		with open("./tests/data/actual_tailored.tex", 'r') as file:
			actual_latex = file.read()
	
		self.assertEqual(expected_latex, actual_latex)

	def test_parse_rendered_latex(self):

		output_path = read_yaml_and_write_latex("./tests/data/test_resume.yaml", "./tests/data/actual_tailored.tex")

		result = subprocess.run(["pdflatex", "-halt-on-error", "-output-directory", "./tests/data", output_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

		self.assertEqual(result.returncode, 0)

	def test_render_latex_to_pdf(self):
		with open("./tests/data/test_resume.yaml", 'r') as file:
			data = yaml.safe_load(file)


		render_data(data, output_pdf_path="./temp")
		
		self.assertTrue(os.path.exists("./temp/tailored_resume.pdf"))