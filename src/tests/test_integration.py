import subprocess
import unittest
from content.tailor import *
from content.render import *

class IntegrationTest(unittest.TestCase):
	def test_tailor_and_render_resume(self):
		with open("./tests/data/test_raw.yaml", 'r') as file:
			data = yaml.safe_load(file)

		with open("./tests/data/test_job_description.txt", "r") as file:
			jd = file.read()

		result = tailor_resume_by_job_description(data, jd)

		self.assertIsNotNone(result)

		tailored_resume = result["resume"]

		latex_string = render_data_to_latex(tailored_resume)

		with open("./tests/data/actual_tailored.tex", 'w') as file:
			file.write(latex_string)


		result = subprocess.run(["pdflatex", "-halt-on-error", "-output-directory", "./tests/data", "./tests/data/actual_tailored.tex"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

		self.assertEqual(result.returncode, 0)